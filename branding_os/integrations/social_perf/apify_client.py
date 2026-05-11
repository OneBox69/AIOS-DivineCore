"""Thin httpx wrapper around the Apify Actor API for LinkedIn + X scrapes.

Mirrors `sales_os/integrations/upwork_jobs/apify_client.py` — one synchronous
HTTP call per platform kicks off a run and returns the scraped items. Apify
rotates its own cookies + proxies, so no LinkedIn/X credentials live on our
side and the ToS risk stays on Apify's side.

If a daily run starts taking longer than ~5 minutes (Apify's synchronous
endpoint times out at 300s), switch to async: POST /runs -> poll
/actor-runs/{id} -> GET dataset items.

The default actor IDs in `worker/settings.py` are reasonable starting points
but actor naming/shape on the Apify Store changes; expect to swap them once
we see real items in the `raw` jsonb column.
"""

from __future__ import annotations

from typing import Any

import httpx

from settings import settings

ACTOR_RUN_TIMEOUT_SECONDS = 300.0


def _api_base() -> str:
    return "https://api.apify.com/v2"


def _actor_path_id(actor_id: str) -> str:
    # Apify accepts both `username/actor-name` and `username~actor-name` —
    # the API path uses the tilde form.
    return actor_id.replace("/", "~")


def run_actor_sync(actor_id: str, input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Run an Apify actor synchronously and return the dataset items.

    Raises RuntimeError if the API token isn't configured. Lets HTTP errors
    propagate so the Celery task can log the actual Apify error response.
    """
    if not settings.APIFY_API_TOKEN:
        raise RuntimeError("APIFY_API_TOKEN not set")

    url = f"{_api_base()}/acts/{_actor_path_id(actor_id)}/run-sync-get-dataset-items"
    headers = {
        "Authorization": f"Bearer {settings.APIFY_API_TOKEN}",
        "Content-Type": "application/json",
    }
    response = httpx.post(url, headers=headers, json=input_payload, timeout=ACTOR_RUN_TIMEOUT_SECONDS)
    response.raise_for_status()
    body = response.json()
    if isinstance(body, list):
        return body
    return []


def fetch_linkedin_posts(profile_url: str, post_limit: int = 50) -> list[dict[str, Any]]:
    """Scrape recent posts off a single LinkedIn profile URL.

    Input shape is the most-common contract across LinkedIn-post actors on
    Apify (profileUrls + max posts). After the first real run, inspect a
    few raw items and tighten or rename fields if the chosen actor uses
    different keys.
    """
    return run_actor_sync(
        settings.APIFY_LINKEDIN_ACTOR_ID,
        {
            "profileUrls": [profile_url],
            "maxPosts": post_limit,
        },
    )


def fetch_x_posts(handle: str, post_limit: int = 50) -> list[dict[str, Any]]:
    """Scrape recent tweets off a single X (Twitter) handle.

    `handle` is the bare username — no leading @, no URL. Most tweet-scraper
    actors accept either `twitterHandles` or `searchTerms=from:handle`; we
    pass both keys so a swap-out only needs `APIFY_X_ACTOR_ID` changed.
    """
    return run_actor_sync(
        settings.APIFY_X_ACTOR_ID,
        {
            "twitterHandles": [handle.lstrip("@")],
            "searchTerms": [f"from:{handle.lstrip('@')}"],
            "maxItems": post_limit,
        },
    )
