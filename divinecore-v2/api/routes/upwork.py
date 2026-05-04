"""Upwork application generator — single-user web form.

GET /upwork    -> render the form
POST /upwork   -> enqueue Celery task, block on result, render the result page
"""

import logging

from celery import Celery
from celery.exceptions import TimeoutError as CeleryTimeoutError
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["upwork"])

_celery = Celery("api", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
_templates = Jinja2Templates(directory="templates")

PIPELINE_TIMEOUT_SECONDS = 180


@router.get("/upwork", response_class=HTMLResponse)
def upwork_form(request: Request):
    return _templates.TemplateResponse("upwork_form.html", {"request": request})


@router.post("/upwork", response_class=HTMLResponse)
def upwork_run(request: Request, job_description: str = Form(...)):
    job_description = job_description.strip()
    if not job_description:
        return _templates.TemplateResponse(
            "upwork_result.html",
            {"request": request, "error": "Job description was empty."},
            status_code=400,
        )

    try:
        async_result = _celery.send_task("tasks.upwork_generate_proposal", args=[job_description])
        result = async_result.get(timeout=PIPELINE_TIMEOUT_SECONDS)
    except CeleryTimeoutError:
        logger.exception("upwork: pipeline timed out after %ss", PIPELINE_TIMEOUT_SECONDS)
        return _templates.TemplateResponse(
            "upwork_result.html",
            {"request": request, "error": f"Pipeline timed out after {PIPELINE_TIMEOUT_SECONDS}s."},
            status_code=504,
        )
    except Exception as exc:
        logger.exception("upwork: pipeline failed")
        return _templates.TemplateResponse(
            "upwork_result.html",
            {"request": request, "error": f"Pipeline failed: {exc}"},
            status_code=500,
        )

    return _templates.TemplateResponse(
        "upwork_result.html",
        {
            "request": request,
            "application_body": result.get("application_body", ""),
            "proposal_url": result.get("proposal_url", ""),
            "script_url": result.get("script_url", ""),
        },
    )
