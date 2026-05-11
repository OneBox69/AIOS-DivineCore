"""Social performance dashboard.

GET /social-perf                  -> dashboard (tabs: linkedin / x / all)
                                    sorted by engagement desc.

The dashboard groups posts by hook / closing / topic / format and shows
median engagement per bucket — so it's easy to spot which opening patterns
actually move the needle. Engagement is `likes + comments + reposts` since
impressions aren't always present (some scrapers can't see them).

Sits behind the same Traefik basicauth as /upwork (see
divinecore-v2/docker-compose.prod.yml).
"""

from __future__ import annotations

import logging
import statistics
from collections import defaultdict
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from branding_os.integrations.social_perf import supabase_writer

logger = logging.getLogger(__name__)

router = APIRouter(tags=["social-perf"])

_templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

VALID_TABS = ("all", "linkedin", "x")


def _engagement(post: dict) -> int:
    m = post.get("metrics") or {}
    return int(m.get("likes", 0) or 0) + int(m.get("comments", 0) or 0) + int(m.get("reposts", 0) or 0)


def _bucket_stats(posts: list[dict], key: str) -> list[dict]:
    """Group posts by `key` (e.g. 'format', 'topic'), return list of
    {bucket, count, median_engagement} sorted by median desc.
    """
    buckets: dict[str, list[int]] = defaultdict(list)
    for p in posts:
        bucket = (p.get(key) or "(unannotated)").strip() or "(unannotated)"
        buckets[bucket].append(_engagement(p))
    rows = [
        {
            "bucket": b,
            "count": len(eng),
            "median_engagement": int(statistics.median(eng)) if eng else 0,
            "max_engagement": max(eng) if eng else 0,
        }
        for b, eng in buckets.items()
    ]
    rows.sort(key=lambda r: (r["median_engagement"], r["count"]), reverse=True)
    return rows


@router.get("/social-perf", response_class=HTMLResponse)
def social_perf_dashboard(request: Request, tab: str = "all"):
    if tab not in VALID_TABS:
        tab = "all"

    platform_filter = None if tab == "all" else tab
    try:
        posts = supabase_writer.fetch_posts(platform=platform_filter, limit=500)
    except Exception as exc:
        logger.exception("social_perf: fetch failed")
        return _templates.TemplateResponse(
            "social_perf_dashboard.html",
            {
                "request": request,
                "tab": tab,
                "posts": [],
                "format_stats": [],
                "topic_stats": [],
                "error": str(exc),
            },
            status_code=500,
        )

    # Decorate + sort by engagement desc for the leaderboard.
    for p in posts:
        p["_engagement"] = _engagement(p)
    posts.sort(key=lambda p: p["_engagement"], reverse=True)

    return _templates.TemplateResponse(
        "social_perf_dashboard.html",
        {
            "request": request,
            "tab": tab,
            "posts": posts,
            "format_stats": _bucket_stats(posts, "format"),
            "topic_stats": _bucket_stats(posts, "topic"),
            "error": None,
        },
    )
