"""Daily social-performance poller + per-post LLM annotator.

Three Celery tasks:

- `tasks.poll_social_posts`     — beat-scheduled. Scrapes every configured
                                  LinkedIn profile + X handle via Apify and
                                  upserts each post to Supabase. Re-fetched
                                  posts refresh metrics without losing
                                  annotations. After the poll, enqueues
                                  `annotate_social_post` for every still-
                                  unannotated row.
- `tasks.annotate_social_post`  — single-post LLM call. Patches hook /
                                  closing / topic / format on the matching
                                  Supabase row.
- `tasks.annotate_backfill`     — manual one-off. Fans out annotation tasks
                                  for every unannotated post. Useful after
                                  changing the prompt or model.

No-ops cleanly when env vars are missing — same safe-deploy pattern as
upwork_jobs / instantly. The list of profiles is comma-separated in env
(`SOCIAL_PERF_LINKEDIN_PROFILES`, `SOCIAL_PERF_X_HANDLES`) so multiple
authors can be tracked without a config table.
"""

from __future__ import annotations

from typing import Any

from celery_app import app
from settings import settings

from . import annotator, apify_client, supabase_writer


# ---------- env parsing ----------

def _split_csv(value: str) -> list[str]:
    if not value:
        return []
    return [chunk.strip() for chunk in value.split(",") if chunk.strip()]


def _linkedin_profiles() -> list[str]:
    return _split_csv(settings.SOCIAL_PERF_LINKEDIN_PROFILES)


def _x_handles() -> list[str]:
    return _split_csv(settings.SOCIAL_PERF_X_HANDLES)


# ---------- LinkedIn normaliser ----------

def _str(value: Any) -> str:
    return "" if value is None else str(value)


def _str_or_none(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value)
    return s if s else None


def _int(value: Any) -> int:
    """Coerce metric counts; many actors return strings like '1.2K'."""
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip().replace(",", "")
    if not s:
        return 0
    multiplier = 1
    if s[-1].lower() in ("k", "m", "b"):
        multiplier = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}[s[-1].lower()]
        s = s[:-1]
    try:
        return int(float(s) * multiplier)
    except ValueError:
        return 0


def _normalise_linkedin(item: dict[str, Any], profile_url: str) -> dict[str, Any] | None:
    """Map an Apify LinkedIn-post item to our schema.

    Field names follow the most common shape across LinkedIn-post actors —
    these will likely need tightening after the first real run. The full
    `raw` payload is preserved so we can adapt without losing data.
    """
    post_id = _str(item.get("urn") or item.get("postId") or item.get("id") or item.get("activityUrn"))
    if not post_id:
        return None

    content = _str(item.get("text") or item.get("postContent") or item.get("commentary"))
    media_type = _str_or_none(item.get("mediaType") or item.get("postType"))

    return {
        "platform": "linkedin",
        "post_id": post_id,
        "author_handle": profile_url,
        "url": _str(item.get("url") or item.get("postUrl") or item.get("link")),
        "posted_at": _str_or_none(item.get("postedAt") or item.get("publishedAt") or item.get("createdAt")),
        "content": content,
        "media_type": media_type,
        "metrics": {
            "likes": _int(item.get("likes") or item.get("numLikes") or item.get("reactionsCount")),
            "comments": _int(item.get("comments") or item.get("numComments") or item.get("commentsCount")),
            "reposts": _int(item.get("reposts") or item.get("shares") or item.get("repostsCount")),
            "impressions": _int(item.get("impressions") or item.get("views")),
        },
        "raw": item,
    }


def _normalise_x(item: dict[str, Any], handle: str) -> dict[str, Any] | None:
    """Map an Apify tweet-scraper item to our schema."""
    post_id = _str(item.get("id") or item.get("tweetId") or item.get("conversationId"))
    if not post_id:
        return None

    content = _str(item.get("text") or item.get("fullText") or item.get("content"))
    return {
        "platform": "x",
        "post_id": post_id,
        "author_handle": handle.lstrip("@"),
        "url": _str(item.get("url") or item.get("tweetUrl") or f"https://x.com/{handle.lstrip('@')}/status/{post_id}"),
        "posted_at": _str_or_none(item.get("createdAt") or item.get("created_at") or item.get("postedAt")),
        "content": content,
        "media_type": _str_or_none(item.get("mediaType") or item.get("type")),
        "metrics": {
            "likes": _int(item.get("likeCount") or item.get("likes") or item.get("favoriteCount")),
            "comments": _int(item.get("replyCount") or item.get("replies")),
            "reposts": _int(item.get("retweetCount") or item.get("retweets")),
            "bookmarks": _int(item.get("bookmarkCount") or item.get("bookmarks")),
            "impressions": _int(item.get("viewCount") or item.get("views") or item.get("impressionsCount")),
        },
        "raw": item,
    }


# ---------- tasks ----------

@app.task(name="tasks.poll_social_posts")
def poll_social_posts() -> dict[str, Any]:
    if not settings.APIFY_API_TOKEN:
        return {"skipped": "APIFY_API_TOKEN not set"}

    linkedin_profiles = _linkedin_profiles()
    x_handles = _x_handles()
    if not linkedin_profiles and not x_handles:
        return {"skipped": "no profiles configured (set SOCIAL_PERF_LINKEDIN_PROFILES or SOCIAL_PERF_X_HANDLES)"}

    summary: dict[str, Any] = {"linkedin": {}, "x": {}, "annotation_enqueued": 0, "errors": []}

    for profile_url in linkedin_profiles:
        try:
            items = apify_client.fetch_linkedin_posts(profile_url)
        except Exception as exc:
            summary["errors"].append({"linkedin": profile_url, "stage": "fetch", "error": str(exc)})
            summary["linkedin"][profile_url] = {"fetched": 0, "upserted": 0}
            continue
        upserted = 0
        for item in items:
            normalised = _normalise_linkedin(item, profile_url)
            if not normalised:
                continue
            try:
                supabase_writer.upsert_post(**normalised)
                upserted += 1
            except Exception as exc:
                summary["errors"].append({"linkedin": profile_url, "stage": "upsert", "post_id": normalised["post_id"], "error": str(exc)})
        summary["linkedin"][profile_url] = {"fetched": len(items), "upserted": upserted}

    for handle in x_handles:
        try:
            items = apify_client.fetch_x_posts(handle)
        except Exception as exc:
            summary["errors"].append({"x": handle, "stage": "fetch", "error": str(exc)})
            summary["x"][handle] = {"fetched": 0, "upserted": 0}
            continue
        upserted = 0
        for item in items:
            normalised = _normalise_x(item, handle)
            if not normalised:
                continue
            try:
                supabase_writer.upsert_post(**normalised)
                upserted += 1
            except Exception as exc:
                summary["errors"].append({"x": handle, "stage": "upsert", "post_id": normalised["post_id"], "error": str(exc)})
        summary["x"][handle] = {"fetched": len(items), "upserted": upserted}

    # Fan out annotation for everything still missing a hook.
    try:
        for row in supabase_writer.fetch_unannotated():
            app.send_task("tasks.annotate_social_post", args=[row["platform"], row["post_id"]])
            summary["annotation_enqueued"] += 1
    except Exception as exc:
        summary["errors"].append({"stage": "annotate-fanout", "error": str(exc)})

    # Trim long error tails for log readability.
    summary["errors"] = summary["errors"][:20]
    return summary


@app.task(name="tasks.annotate_social_post")
def annotate_social_post(platform: str, post_id: str) -> dict[str, Any]:
    posts = supabase_writer.fetch_posts(platform=platform, limit=500)
    target = next((p for p in posts if p.get("post_id") == post_id), None)
    if not target:
        return {"skipped": f"{platform}:{post_id} not found"}
    if target.get("hook"):
        return {"skipped": f"{platform}:{post_id} already annotated"}

    content = (target.get("content") or "").strip()
    if not content:
        return {"skipped": f"{platform}:{post_id} empty content"}

    try:
        parsed = annotator.annotate(content)
    except annotator.AnnotationError as exc:
        return {"error": str(exc), "platform": platform, "post_id": post_id}

    supabase_writer.set_annotation(
        platform=platform,
        post_id=post_id,
        hook=parsed["hook"],
        closing=parsed["closing"],
        topic=parsed["topic"],
        format_=parsed["format"],
        annotator_model=settings.SOCIAL_PERF_ANNOTATOR_MODEL,
    )
    return {"annotated": f"{platform}:{post_id}", "format": parsed["format"], "topic": parsed["topic"]}


@app.task(name="tasks.annotate_backfill")
def annotate_backfill() -> dict[str, Any]:
    enqueued = 0
    for row in supabase_writer.fetch_unannotated(limit=1000):
        app.send_task("tasks.annotate_social_post", args=[row["platform"], row["post_id"]])
        enqueued += 1
    return {"enqueued": enqueued}
