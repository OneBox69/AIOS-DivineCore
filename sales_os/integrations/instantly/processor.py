"""Celery tasks for the Instantly integration.

Two entry points:
- `tasks.process_instantly_reply` — invoked by the FastAPI webhook handler in
  `sales_os/web/instantly_routes.py`. Stores meaningful replies, pings Discord
  on positive ones.
- `tasks.poll_instantly_campaigns` — invoked daily by Celery Beat. Snapshots
  Instantly's campaign + step analytics into Supabase.

Webhook payload shapes vary by Instantly plan. The reply extractor below
reads from several common field names (`lead_email`, `email`, `from_email`,
etc.) and falls back to empty values rather than crashing — the full raw
payload is always stored in `outreach_replies.raw_payload` for forensics.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any

from celery_app import app

from . import categories, client, discord_notify, supabase_writer


# ---------- reply payload extraction ----------

def _first(payload: dict, *keys: str) -> Any:
    for k in keys:
        if k in payload and payload[k] not in (None, ""):
            return payload[k]
    return None


def _nested(payload: dict, path: list[str]) -> Any:
    cur: Any = payload
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
        if cur in (None, ""):
            return None
    return cur


def _extract_reply(payload: dict) -> dict[str, Any]:
    lead = payload.get("lead") if isinstance(payload.get("lead"), dict) else {}
    campaign = payload.get("campaign") if isinstance(payload.get("campaign"), dict) else {}
    reply = payload.get("reply") if isinstance(payload.get("reply"), dict) else {}

    return {
        "instantly_lead_id": (
            _first(payload, "lead_id", "instantly_lead_id")
            or lead.get("id")
            or lead.get("lead_id")
        ),
        "lead_email": (
            _first(payload, "lead_email", "email", "from_email", "reply_from_email")
            or lead.get("email")
            or ""
        ),
        "lead_company": (
            _first(payload, "company", "company_name")
            or lead.get("company")
            or lead.get("company_name")
        ),
        "campaign_id": (
            _first(payload, "campaign_id", "instantly_campaign_id")
            or campaign.get("id")
            or campaign.get("campaign_id")
        ),
        "campaign_name": (
            _first(payload, "campaign_name") or campaign.get("name")
        ),
        "step_index": (
            _first(payload, "step", "step_index", "email_position", "sequence_step")
            or reply.get("step")
            or reply.get("step_index")
        ),
        "replied_at": (
            _first(payload, "replied_at", "received_at", "timestamp", "event_timestamp")
            or reply.get("received_at")
            or datetime.now(timezone.utc).isoformat()
        ),
        "body": (
            _first(payload, "reply_text", "body", "message", "reply_body")
            or reply.get("text")
            or reply.get("body")
        ),
        "instantly_category": (
            _first(payload, "category", "lead_category", "lead_status", "interest", "ai_category")
            or lead.get("status")
            or lead.get("category")
        ),
        "reply_url": _first(payload, "reply_url", "thread_url", "url"),
    }


def _coerce_step(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


@app.task(name="tasks.process_instantly_reply")
def process_instantly_reply(payload: dict) -> dict:
    fields = _extract_reply(payload)
    category = fields["instantly_category"]

    if categories.is_ignored(category):
        return {"skipped": "ignored_category", "category": category}

    is_positive = categories.is_positive(category)

    reply_row = supabase_writer.insert_reply(
        instantly_lead_id=fields["instantly_lead_id"],
        lead_email=fields["lead_email"] or "unknown@unknown",
        lead_company=fields["lead_company"],
        campaign_id=fields["campaign_id"],
        step_index=_coerce_step(fields["step_index"]),
        replied_at=fields["replied_at"],
        body=fields["body"],
        instantly_category=category,
        is_positive=is_positive,
        reply_url=fields["reply_url"],
        raw_payload=payload,
    )

    if not is_positive:
        return {
            "stored": True,
            "reply_id": reply_row.get("id"),
            "category": category,
            "discord": "skipped (not positive)",
        }

    positioning = None
    campaign_name = fields["campaign_name"]
    if fields["campaign_id"]:
        try:
            campaign_row = supabase_writer.fetch_campaign(fields["campaign_id"])
            if campaign_row:
                positioning = campaign_row.get("positioning") or None
                campaign_name = campaign_name or campaign_row.get("name")
        except Exception as exc:
            print(f"[instantly] fetch_campaign failed (non-fatal): {exc}", flush=True)

    try:
        posted = discord_notify.post_positive_reply(
            lead_email=fields["lead_email"] or "unknown",
            lead_company=fields["lead_company"],
            campaign_name=campaign_name,
            positioning=positioning,
            instantly_category=category,
            body=fields["body"],
            reply_url=fields["reply_url"],
        )
    except Exception as exc:
        print(f"[instantly] discord_notify failed (non-fatal): {exc}", flush=True)
        posted = False

    return {
        "stored": True,
        "reply_id": reply_row.get("id"),
        "category": category,
        "discord": "posted" if posted else "skipped (no webhook)",
    }


# ---------- daily snapshot ----------

# Field names returned by Instantly's /campaigns/analytics{,/steps} endpoints.
# Verified against live payloads stored in raw_snapshot. We prefer the unique_*
# variants where they exist (e.g. unique_replies dedupes multi-replies from the
# same lead — that's the count users care about for reply-rate metrics).
# Open and bounce fields are intentionally not extracted — Instantly returns
# 0 for opens on these campaigns (no pixel tracking) and the operator has
# decided neither metric is worth surfacing.
_SENT_KEYS = ("sent", "emails_sent_count", "total_sent", "email_sent_count")
_REPLIED_KEYS = ("unique_replies", "replies", "emails_replied_count", "replied", "total_replies", "reply_count")
_UNSUB_KEYS = ("unsubscribes", "unsubscribed", "unsubscribe_count", "total_unsubscribes")


def _sum_int(blob: dict, keys: tuple[str, ...]) -> int:
    for k in keys:
        if k in blob and blob[k] is not None:
            try:
                return int(blob[k])
            except (TypeError, ValueError):
                continue
    return 0


def _campaign_name(c: dict) -> str:
    return c.get("name") or c.get("campaign_name") or "(unnamed)"


def _campaign_status(c: dict) -> str:
    raw = c.get("status")
    if isinstance(raw, str):
        return raw
    if isinstance(raw, int):
        return f"status_{raw}"
    return ""


def _campaign_started_at(c: dict) -> str | None:
    return c.get("created_at") or c.get("started_at") or c.get("launch_date")


def _snapshot_one_campaign(campaign: dict, snapshot_date: date) -> dict:
    campaign_id = str(campaign.get("id") or campaign.get("campaign_id") or "")
    if not campaign_id:
        return {"skipped": "no campaign id"}

    supabase_writer.upsert_campaign(
        campaign_id=campaign_id,
        name=_campaign_name(campaign),
        status=_campaign_status(campaign),
        started_at=_campaign_started_at(campaign),
    )

    overall = client.get_campaign_analytics(campaign_id)
    steps = client.get_campaign_steps_analytics(campaign_id)

    metrics_rows: list[dict] = []

    if steps:
        for s in steps:
            step_index = int(s.get("step") or s.get("step_index") or s.get("position") or 1)
            supabase_writer.upsert_sequence_step(
                campaign_id=campaign_id,
                step_index=step_index,
                subject=s.get("subject"),
                body_preview=s.get("body") or s.get("body_preview"),
            )
            row = supabase_writer.upsert_daily_metrics(
                campaign_id=campaign_id,
                step_index=step_index,
                metrics_date=snapshot_date,
                emails_sent=_sum_int(s, _SENT_KEYS),
                replies=_sum_int(s, _REPLIED_KEYS),
                unsubscribes=_sum_int(s, _UNSUB_KEYS),
                raw_snapshot=s,
            )
            metrics_rows.append(row)
    else:
        # Fallback: one rolled-up row at step_index=0 when per-step analytics
        # isn't available on the plan.
        row = supabase_writer.upsert_daily_metrics(
            campaign_id=campaign_id,
            step_index=0,
            metrics_date=snapshot_date,
            emails_sent=_sum_int(overall, _SENT_KEYS),
            replies=_sum_int(overall, _REPLIED_KEYS),
            unsubscribes=_sum_int(overall, _UNSUB_KEYS),
            raw_snapshot=overall,
        )
        metrics_rows.append(row)

    return {"campaign_id": campaign_id, "rows_written": len(metrics_rows)}


@app.task(name="tasks.poll_instantly_campaigns")
def poll_instantly_campaigns() -> dict:
    from settings import settings

    if not settings.INSTANTLY_API_KEY:
        return {"skipped": "INSTANTLY_API_KEY not set"}

    snapshot_date = (datetime.now(timezone.utc) - timedelta(days=1)).date()
    campaigns = client.list_campaigns()
    results: list[dict] = []
    for c in campaigns:
        try:
            results.append(_snapshot_one_campaign(c, snapshot_date))
        except Exception as exc:
            print(f"[instantly] snapshot failed for {c.get('id')}: {exc}", flush=True)
            results.append({"campaign_id": c.get("id"), "error": str(exc)})
    return {
        "snapshot_date": snapshot_date.isoformat(),
        "campaigns_seen": len(campaigns),
        "results": results,
    }
