"""Daily Upwork job-feed poller.

Beat fires `tasks.poll_upwork_jobs` once a day at 21:40 UTC (= 05:40 MYT).
The task scrapes `UPWORK_SEARCH_URL` via the configured Apify actor,
normalises each item to our column set, and upserts into the `upwork_jobs`
Supabase table. The full Apify item is preserved in the `raw` column so we
can adapt to shape changes without losing data.

No-op (returns a `skipped` payload) if either UPWORK_SEARCH_URL or
APIFY_API_TOKEN is missing — keeps the runtime safe to deploy before the
team has paid for Apify and before the search URL is decided.
"""

from __future__ import annotations

from typing import Any

from celery_app import app
from settings import settings

from . import apify_client, supabase_writer


def _str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _str_or_none(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value)
    return s if s else None


def _list_str(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(v) for v in value if v is not None]


def _list_str_or_none(value: Any) -> list[str] | None:
    """`allowedApplicantCountries` is null when there are no restrictions
    and a list when there are. Preserve the null-vs-empty distinction so
    the UI can render "(open to all)" vs "(restricted to: …)".
    """
    if value is None:
        return None
    if not isinstance(value, list):
        return None
    return [str(v) for v in value if v is not None]


def _dict(value: Any) -> dict | None:
    return value if isinstance(value, dict) else None


def _normalise(item: dict[str, Any]) -> dict[str, Any] | None:
    """Map an Apify-shaped Upwork job item to our column set.

    Field names follow the actor's documented output. Falls back through
    several common alternates (`id` / `jobId` / `ciphertext`) to absorb
    minor shape changes without crashing. Returns None if no usable
    primary key can be found — those items are skipped, not stored.
    """
    job_id = _str(item.get("id") or item.get("jobId") or item.get("ciphertext"))
    if not job_id:
        return None

    return {
        "job_id": job_id,
        "url": _str(item.get("url") or item.get("jobUrl")),
        "title": _str(item.get("title")),
        "description": _str(item.get("description")),
        "budget": _dict(item.get("budget") or item.get("hourlyBudget") or item.get("amount")),
        "client_stats": _dict(item.get("client") or item.get("clientStats")),
        "skills": _list_str(item.get("skills") or item.get("ontologySkills")),
        "posted_at": _str_or_none(
            item.get("postedOn") or item.get("publishedOn") or item.get("createdAt")
        ),
        "tags": _list_str(item.get("tags")),
        "contract_type": _str_or_none(item.get("contractType") or item.get("type")),
        "engagement": _str_or_none(item.get("engagement") or item.get("duration")),
        "country_restrictions": _list_str_or_none(item.get("allowedApplicantCountries")),
        "experience_level": _str_or_none(item.get("experienceLevel") or item.get("tier")),
        "category": _str_or_none(item.get("category") or item.get("subcategory")),
        "raw": item,
    }


@app.task(name="tasks.poll_upwork_jobs")
def poll_upwork_jobs() -> dict[str, Any]:
    if not settings.APIFY_API_TOKEN:
        return {"skipped": "APIFY_API_TOKEN not set"}
    if not settings.UPWORK_SEARCH_URL:
        return {"skipped": "UPWORK_SEARCH_URL not set"}

    items = apify_client.fetch_upwork_jobs(settings.UPWORK_SEARCH_URL)

    upserted = 0
    skipped_missing_id = 0
    errors: list[dict[str, Any]] = []
    for item in items:
        normalised = _normalise(item)
        if not normalised:
            skipped_missing_id += 1
            continue
        try:
            supabase_writer.upsert_job(**normalised)
            upserted += 1
        except Exception as exc:
            print(f"[upwork_jobs] upsert failed for {normalised.get('job_id')}: {exc}", flush=True)
            errors.append({"job_id": normalised.get("job_id"), "error": str(exc)})

    return {
        "fetched": len(items),
        "upserted": upserted,
        "skipped_missing_id": skipped_missing_id,
        "errors": errors[:10],
    }
