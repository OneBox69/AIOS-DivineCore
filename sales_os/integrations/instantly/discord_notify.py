"""Discord embed for positive replies.

Posts to a webhook on `#sales-and-outreach`, targeted into the dedicated
`outreach-replies` thread via the `?thread_id=` query parameter. No-op if
either env var is unset (so the integration still works pre-Discord wiring).
"""

from __future__ import annotations

import httpx

from settings import settings

POSITIVE_COLOR = 0x2ECC71  # green
SNIPPET_LIMIT = 800


def _snippet(body: str | None) -> str:
    if not body:
        return "_(empty body)_"
    text = body.strip()
    if len(text) <= SNIPPET_LIMIT:
        return text
    return text[:SNIPPET_LIMIT] + "…"


def post_positive_reply(
    *,
    lead_email: str,
    lead_company: str | None,
    campaign_name: str | None,
    positioning: str | None,
    instantly_category: str | None,
    body: str | None,
    reply_url: str | None,
) -> bool:
    webhook = settings.DISCORD_OUTREACH_WEBHOOK_URL
    if not webhook:
        return False

    fields = [
        {"name": "Lead", "value": lead_email or "_(unknown)_", "inline": True},
        {"name": "Company", "value": lead_company or "_(unknown)_", "inline": True},
        {"name": "Category", "value": instantly_category or "_(unlabeled)_", "inline": True},
        {"name": "Campaign", "value": campaign_name or "_(unknown)_", "inline": True},
        {"name": "Positioning", "value": positioning or "_(unset)_", "inline": True},
    ]

    embed = {
        "title": "Positive reply",
        "color": POSITIVE_COLOR,
        "description": _snippet(body),
        "fields": fields,
    }
    if reply_url:
        embed["url"] = reply_url

    url = webhook
    if settings.DISCORD_OUTREACH_THREAD_ID:
        sep = "&" if "?" in webhook else "?"
        url = f"{webhook}{sep}thread_id={settings.DISCORD_OUTREACH_THREAD_ID}"

    response = httpx.post(url, json={"embeds": [embed]}, timeout=10.0)
    response.raise_for_status()
    return True
