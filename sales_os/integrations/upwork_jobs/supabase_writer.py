"""PostgREST writers + readers for the `upwork_jobs` table.

Same auth + on_conflict pattern as `ops_os/integrations/fathom/supabase_writer.py`
and `sales_os/integrations/instantly/supabase_writer.py`.

Operator-owned columns — `status`, `reviewed_at`, `applied_at`,
`proposal_doc_url` — are never touched by the daily upsert. They're only
written by `update_status()`, which is called from the queue UI button
handlers. The rest of the row (description, client stats, etc.) is merge-
replaced on conflict so re-fetched jobs get fresh data without the operator
losing their review state.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx

from settings import settings

JOBS_TABLE = "upwork_jobs"

# Columns the daily poller writes. Excludes status / reviewed_at /
# applied_at / proposal_doc_url — those are operator-owned. PostgREST's
# `?columns=` whitelists which fields are sent on insert *and* update, so
# leaving them off here means a reviewed-then-re-scraped job keeps its
# review state intact.
POLLER_COLUMNS = (
    "job_id,url,title,description,budget,client_stats,skills,posted_at,"
    "tags,contract_type,engagement,country_restrictions,experience_level,"
    "category,raw,fetched_at"
)


def _headers(prefer: str) -> dict[str, str]:
    return {
        "apikey": settings.SUPABASE_SECRET_KEY,
        "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
        "Content-Type": "application/json",
        "Prefer": prefer,
    }


def _rest_base() -> str:
    return f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1"


def upsert_job(
    *,
    job_id: str,
    url: str,
    title: str,
    description: str,
    budget: dict | None,
    client_stats: dict | None,
    skills: list[str] | None,
    posted_at: str | None,
    tags: list[str] | None,
    contract_type: str | None,
    engagement: str | None,
    country_restrictions: list[str] | None,
    experience_level: str | None,
    category: str | None,
    raw: dict,
) -> dict[str, Any]:
    row = {
        "job_id": job_id,
        "url": url,
        "title": title,
        "description": description,
        "budget": budget or {},
        "client_stats": client_stats or {},
        "skills": skills or [],
        "posted_at": posted_at,
        "tags": tags or [],
        "contract_type": contract_type,
        "engagement": engagement,
        "country_restrictions": country_restrictions,
        "experience_level": experience_level,
        "category": category,
        "raw": raw,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    rest_url = (
        f"{_rest_base()}/{JOBS_TABLE}"
        f"?on_conflict=job_id&columns={POLLER_COLUMNS}"
    )
    response = httpx.post(
        rest_url,
        headers=_headers("resolution=merge-duplicates,return=representation"),
        json=[row],
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return (data or [row])[0]


def fetch_jobs_by_status(status: str, limit: int = 200) -> list[dict[str, Any]]:
    rest_url = (
        f"{_rest_base()}/{JOBS_TABLE}"
        f"?status=eq.{status}&order=posted_at.desc.nullslast&limit={limit}"
    )
    response = httpx.get(rest_url, headers=_headers("count=exact"), timeout=30.0)
    response.raise_for_status()
    return response.json() or []


def count_jobs_by_status(status: str) -> int:
    rest_url = (
        f"{_rest_base()}/{JOBS_TABLE}"
        f"?status=eq.{status}&select=job_id"
    )
    response = httpx.get(
        rest_url,
        headers={**_headers("count=exact"), "Range-Unit": "items", "Range": "0-0"},
        timeout=30.0,
    )
    # Status 206 (Partial Content) is normal for Range queries; raise on real errors.
    if response.status_code not in (200, 206):
        response.raise_for_status()
    content_range = response.headers.get("Content-Range", "")
    # Format: "0-0/123" or "*/0"
    if "/" in content_range:
        total = content_range.split("/", 1)[1]
        if total.isdigit():
            return int(total)
    return len(response.json() or [])


def fetch_job(job_id: str) -> dict[str, Any] | None:
    rest_url = (
        f"{_rest_base()}/{JOBS_TABLE}"
        f"?job_id=eq.{job_id}&select=*&limit=1"
    )
    response = httpx.get(rest_url, headers=_headers("count=exact"), timeout=30.0)
    response.raise_for_status()
    rows = response.json() or []
    return rows[0] if rows else None


def update_status(
    job_id: str,
    status: str,
    *,
    proposal_doc_url: str | None = None,
) -> dict[str, Any] | None:
    """Flip a job's review status.

    - status='skipped'  -> sets reviewed_at = now()
    - status='applied'  -> sets reviewed_at = applied_at = now(), plus proposal_doc_url if provided
    - status='new'      -> clears reviewed_at / applied_at / proposal_doc_url so the row looks fresh
                           when un-skipping or un-marking applied
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    if status == "applied":
        patch: dict[str, Any] = {
            "status": "applied",
            "reviewed_at": now_iso,
            "applied_at": now_iso,
        }
        if proposal_doc_url:
            patch["proposal_doc_url"] = proposal_doc_url
    elif status == "skipped":
        patch = {
            "status": "skipped",
            "reviewed_at": now_iso,
        }
    elif status == "new":
        patch = {
            "status": "new",
            "reviewed_at": None,
            "applied_at": None,
            "proposal_doc_url": None,
        }
    else:
        raise ValueError(f"update_status: unsupported status {status!r}")

    rest_url = f"{_rest_base()}/{JOBS_TABLE}?job_id=eq.{job_id}"
    response = httpx.patch(
        rest_url,
        headers=_headers("return=representation"),
        json=patch,
        timeout=30.0,
    )
    response.raise_for_status()
    rows = response.json() or []
    return rows[0] if rows else None
