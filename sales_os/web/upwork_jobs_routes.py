"""Upwork job-feed review queue.

Daily Apify scrape lands in the `upwork_jobs` Supabase table; this router
exposes the manual review UI on top of it.

GET  /upwork-jobs                       -> queue list (tabs: new / skipped / applied)
GET  /upwork-jobs/{job_id}              -> single-job detail
POST /upwork-jobs/{id}/skip             -> status='skipped'
POST /upwork-jobs/{id}/unskip           -> status='new' (back to queue)
POST /upwork-jobs/{id}/unmark-applied   -> status='new' (recover from accidental click)
POST /upwork-jobs/{id}/generate         -> run the existing Upwork pipeline with the
                                           stored description, mark 'applied' on
                                           success, render the standard upwork_result page.

All routes sit behind the same Traefik basicauth as /upwork (router 'upwork',
priority 10 — see divinecore-v2/docker-compose.prod.yml).
"""

from __future__ import annotations

import logging
from pathlib import Path

from celery import Celery
from celery.exceptions import TimeoutError as CeleryTimeoutError
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sales_os.integrations.upwork_jobs import supabase_writer
from settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["upwork-jobs"])

_celery = Celery("api", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
_templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

PIPELINE_TIMEOUT_SECONDS = 180

VALID_TABS = ("new", "skipped", "applied")


def _tab_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in VALID_TABS:
        try:
            counts[t] = supabase_writer.count_jobs_by_status(t)
        except Exception:
            logger.exception("upwork_jobs: count failed for tab %s", t)
            counts[t] = 0
    return counts


@router.get("/upwork-jobs", response_class=HTMLResponse)
def upwork_jobs_list(request: Request, tab: str = "new"):
    if tab not in VALID_TABS:
        tab = "new"

    try:
        jobs = supabase_writer.fetch_jobs_by_status(tab)
        counts = _tab_counts()
    except Exception as exc:
        logger.exception("upwork_jobs: list query failed")
        return _templates.TemplateResponse(
            "upwork_jobs_list.html",
            {
                "request": request,
                "jobs": [],
                "tab": tab,
                "counts": {t: 0 for t in VALID_TABS},
                "error": str(exc),
            },
            status_code=500,
        )

    return _templates.TemplateResponse(
        "upwork_jobs_list.html",
        {"request": request, "jobs": jobs, "tab": tab, "counts": counts, "error": None},
    )


@router.get("/upwork-jobs/{job_id}", response_class=HTMLResponse)
def upwork_jobs_detail(request: Request, job_id: str):
    try:
        job = supabase_writer.fetch_job(job_id)
    except Exception as exc:
        logger.exception("upwork_jobs: detail query failed")
        return _templates.TemplateResponse(
            "upwork_jobs_detail.html",
            {"request": request, "job": None, "error": str(exc)},
            status_code=500,
        )
    if not job:
        return _templates.TemplateResponse(
            "upwork_jobs_detail.html",
            {"request": request, "job": None, "error": f"Job {job_id} not found"},
            status_code=404,
        )
    return _templates.TemplateResponse(
        "upwork_jobs_detail.html",
        {"request": request, "job": job, "error": None},
    )


@router.post("/upwork-jobs/{job_id}/skip")
def upwork_jobs_skip(job_id: str):
    try:
        supabase_writer.update_status(job_id, "skipped")
    except Exception as exc:
        logger.exception("upwork_jobs: skip failed")
        raise HTTPException(status_code=500, detail=f"Skip failed: {exc}")
    return RedirectResponse(url="/upwork-jobs?tab=new", status_code=303)


@router.post("/upwork-jobs/{job_id}/unskip")
def upwork_jobs_unskip(job_id: str):
    try:
        supabase_writer.update_status(job_id, "new")
    except Exception as exc:
        logger.exception("upwork_jobs: unskip failed")
        raise HTTPException(status_code=500, detail=f"Unskip failed: {exc}")
    return RedirectResponse(url="/upwork-jobs?tab=skipped", status_code=303)


@router.post("/upwork-jobs/{job_id}/unmark-applied")
def upwork_jobs_unmark_applied(job_id: str):
    try:
        supabase_writer.update_status(job_id, "new")
    except Exception as exc:
        logger.exception("upwork_jobs: unmark-applied failed")
        raise HTTPException(status_code=500, detail=f"Unmark failed: {exc}")
    return RedirectResponse(url="/upwork-jobs?tab=applied", status_code=303)


@router.post("/upwork-jobs/{job_id}/generate", response_class=HTMLResponse)
def upwork_jobs_generate(request: Request, job_id: str):
    try:
        job = supabase_writer.fetch_job(job_id)
    except Exception as exc:
        logger.exception("upwork_jobs: fetch for generate failed")
        return _templates.TemplateResponse(
            "upwork_result.html",
            {"request": request, "error": f"Failed to fetch job: {exc}"},
            status_code=500,
        )
    if not job:
        return _templates.TemplateResponse(
            "upwork_result.html",
            {"request": request, "error": f"Job {job_id} not found"},
            status_code=404,
        )

    description = (job.get("description") or "").strip()
    if not description:
        return _templates.TemplateResponse(
            "upwork_result.html",
            {"request": request, "error": "Stored job description is empty."},
            status_code=400,
        )

    try:
        async_result = _celery.send_task("tasks.upwork_generate_proposal", args=[description])
        result = async_result.get(timeout=PIPELINE_TIMEOUT_SECONDS)
    except CeleryTimeoutError:
        logger.exception("upwork_jobs: pipeline timed out after %ss", PIPELINE_TIMEOUT_SECONDS)
        return _templates.TemplateResponse(
            "upwork_result.html",
            {"request": request, "error": f"Pipeline timed out after {PIPELINE_TIMEOUT_SECONDS}s."},
            status_code=504,
        )
    except Exception as exc:
        logger.exception("upwork_jobs: pipeline failed")
        return _templates.TemplateResponse(
            "upwork_result.html",
            {"request": request, "error": f"Pipeline failed: {exc}"},
            status_code=500,
        )

    proposal_url = result.get("proposal_url", "")
    try:
        supabase_writer.update_status(job_id, "applied", proposal_doc_url=proposal_url)
    except Exception:
        # Non-fatal: proposal succeeded; status flip can be redone manually.
        logger.exception("upwork_jobs: failed to flip status to applied (non-fatal)")

    return _templates.TemplateResponse(
        "upwork_result.html",
        {
            "request": request,
            "application_body": result.get("application_body", ""),
            "proposal_url": proposal_url,
            "row_index": result.get("row_index", -1),
        },
    )
