"""LLM annotator — extracts hook / closing / topic / format from post text.

One OpenRouter call per post. Output is a tight JSON object; we ask the
model to be conservative (literal hook + closing copied from the post,
short single-word topic, format from a fixed enum). Same OpenRouter setup
as the existing Fathom categorizer + Upwork pipeline.

Run via the `tasks.annotate_social_post` Celery task — never call this
inline from the poller, since LLM latency would block the poll loop.
"""

from __future__ import annotations

import json
from typing import Any

import httpx

from settings import settings

ANNOTATOR_SYSTEM_PROMPT = """You analyse short-form social posts (LinkedIn / X).

Return ONLY a JSON object with these exact keys:
- "hook":    the post's opening — the first 1–2 sentences as written, verbatim. No paraphrasing.
- "closing": the post's last 1–2 sentences as written, verbatim. If the post is one line, repeat the hook.
- "topic":   1–3 word topic tag (e.g. "AI agents", "cold outreach", "personal story").
- "format":  ONE of: list, story, insight, question, case-study, hot-take, tutorial, announcement, other.

No prose. No markdown fences. Just the JSON object."""

# Format enum mirrors the system prompt — used to clamp model drift to a known set.
VALID_FORMATS = {
    "list",
    "story",
    "insight",
    "question",
    "case-study",
    "hot-take",
    "tutorial",
    "announcement",
    "other",
}


class AnnotationError(RuntimeError):
    pass


def annotate(content: str) -> dict[str, str]:
    """Call OpenRouter, return a dict with hook/closing/topic/format keys.

    Raises AnnotationError on missing config or malformed model output —
    let the Celery task layer handle retry / logging.
    """
    if not settings.OPENROUTER_API_KEY:
        raise AnnotationError("OPENROUTER_API_KEY not set")
    if not content.strip():
        raise AnnotationError("empty content")

    url = f"{settings.OPENROUTER_BASE_URL.rstrip('/')}/chat/completions"
    payload: dict[str, Any] = {
        "model": settings.SOCIAL_PERF_ANNOTATOR_MODEL,
        "messages": [
            {"role": "system", "content": ANNOTATOR_SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
    }
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    response = httpx.post(url, headers=headers, json=payload, timeout=60.0)
    response.raise_for_status()
    body = response.json()
    try:
        raw_text = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AnnotationError(f"unexpected OpenRouter response shape: {body}") from exc

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise AnnotationError(f"model did not return JSON: {raw_text!r}") from exc

    hook = str(parsed.get("hook", "")).strip()
    closing = str(parsed.get("closing", "")).strip()
    topic = str(parsed.get("topic", "")).strip()
    fmt = str(parsed.get("format", "")).strip().lower()
    if fmt not in VALID_FORMATS:
        fmt = "other"

    if not (hook and closing and topic):
        raise AnnotationError(f"model missing required fields: {parsed!r}")

    return {"hook": hook, "closing": closing, "topic": topic, "format": fmt}
