"""PostgREST writers + readers for the `social_posts` table.

Same auth + on_conflict pattern as the other Supabase writers in the repo
(see `sales_os/integrations/upwork_jobs/supabase_writer.py`).

Primary key is composite `(platform, post_id)` so LinkedIn and X never
collide on a shared numeric/string id.

Two write paths:
  - `upsert_post(...)` — daily poller. Writes everything except annotation
    columns, so re-fetching a post refreshes its metrics without wiping the
    LLM-extracted hook/closing/topic/format.
  - `set_annotation(...)` — the annotator task. Patches just the four
    annotation columns + `annotated_at` + `annotator_model`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx

from settings import settings

POSTS_TABLE = "social_posts"

# Columns the daily poller writes. Excludes hook / closing / topic / format /
# annotated_at / annotator_model — those are owned by the annotator task.
POLLER_COLUMNS = (
    "platform,post_id,author_handle,url,posted_at,content,media_type,"
    "metrics,raw,fetched_at,metrics_updated_at"
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


def upsert_post(
    *,
    platform: str,
    post_id: str,
    author_handle: str,
    url: str,
    posted_at: str | None,
    content: str,
    media_type: str | None,
    metrics: dict[str, Any],
    raw: dict[str, Any],
) -> dict[str, Any]:
    now_iso = datetime.now(timezone.utc).isoformat()
    row = {
        "platform": platform,
        "post_id": post_id,
        "author_handle": author_handle,
        "url": url,
        "posted_at": posted_at,
        "content": content,
        "media_type": media_type,
        "metrics": metrics or {},
        "raw": raw,
        "fetched_at": now_iso,
        "metrics_updated_at": now_iso,
    }
    rest_url = (
        f"{_rest_base()}/{POSTS_TABLE}"
        f"?on_conflict=platform,post_id&columns={POLLER_COLUMNS}"
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


def fetch_unannotated(limit: int = 100) -> list[dict[str, Any]]:
    """Posts that haven't been through the annotator yet (hook is null)."""
    rest_url = (
        f"{_rest_base()}/{POSTS_TABLE}"
        f"?hook=is.null&order=posted_at.desc.nullslast&limit={limit}"
    )
    response = httpx.get(rest_url, headers=_headers("count=exact"), timeout=30.0)
    response.raise_for_status()
    return response.json() or []


def fetch_posts(
    *,
    platform: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """All posts (optionally filtered by platform), newest first."""
    filters: list[str] = []
    if platform:
        filters.append(f"platform=eq.{platform}")
    filters.append("order=posted_at.desc.nullslast")
    filters.append(f"limit={limit}")
    rest_url = f"{_rest_base()}/{POSTS_TABLE}?{'&'.join(filters)}"
    response = httpx.get(rest_url, headers=_headers("count=exact"), timeout=30.0)
    response.raise_for_status()
    return response.json() or []


def set_annotation(
    *,
    platform: str,
    post_id: str,
    hook: str,
    closing: str,
    topic: str,
    format_: str,
    annotator_model: str,
) -> dict[str, Any] | None:
    patch = {
        "hook": hook,
        "closing": closing,
        "topic": topic,
        "format": format_,
        "annotated_at": datetime.now(timezone.utc).isoformat(),
        "annotator_model": annotator_model,
    }
    rest_url = (
        f"{_rest_base()}/{POSTS_TABLE}"
        f"?platform=eq.{platform}&post_id=eq.{post_id}"
    )
    response = httpx.patch(
        rest_url,
        headers=_headers("return=representation"),
        json=patch,
        timeout=30.0,
    )
    response.raise_for_status()
    rows = response.json() or []
    return rows[0] if rows else None
