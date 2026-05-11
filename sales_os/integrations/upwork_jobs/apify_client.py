"""Thin httpx wrapper around the Apify Actor API.

Calls `run-sync-get-dataset-items` so a single HTTP request kicks off a run
and returns the scraped items in the same response. Apify rotates its own
cookies + proxies, so no Upwork credentials are ever required on our side —
the ToS risk lives with Apify, not Pang's account.

If the daily run starts taking longer than ~5 minutes (Apify pushes the
synchronous endpoint to time out at 300s), switch to the async pattern:
POST /v2/acts/{id}/runs -> poll /v2/actor-runs/{id} -> GET dataset items.
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


def fetch_upwork_jobs(raw_url: str, results_per_page: int = 50) -> list[dict[str, Any]]:
    """Call the configured Upwork job-scraper actor with a raw Upwork search URL.

    Per the actor's docs, `rawUrl` overrides other input parameters, so the
    operator controls all filters via the URL itself (recency, experience
    level, budget, etc.). `resultsPerPage` is a safe override even when
    `rawUrl` is set.
    """
    return run_actor_sync(
        settings.APIFY_UPWORK_ACTOR_ID,
        {
            "rawUrl": raw_url,
            "resultsPerPage": results_per_page,
        },
    )
