"""Celery task entry point for the Upwork pipeline."""

import logging
from datetime import datetime, timezone

from celery_app import app

from . import config, google_client, llm

logger = logging.getLogger(__name__)


@app.task(name="tasks.upwork_generate_proposal")
def upwork_generate_proposal(job_description: str) -> dict:
    logger.info("upwork: generating proposal fields")
    fields = llm.proposal_fields(job_description)
    title = fields.get("titleOfSystem") or "Untitled proposal"

    logger.info("upwork: generating mermaid diagram")
    diagram = llm.mermaid(job_description)

    logger.info("upwork: generating application copy")
    application_body = llm.application_copy(job_description)

    logger.info("upwork: copying proposal doc from template %s", config.PROPOSAL_TEMPLATE_ID)
    proposal_id = google_client.copy_doc(config.PROPOSAL_TEMPLATE_ID, f"[Automation] {title}")
    google_client.share_doc(proposal_id, role="reader")
    google_client.fill_doc(
        proposal_id,
        {
            "titleOfSystem": fields.get("titleOfSystem", ""),
            "briefExplanationOfSystem": fields.get("briefExplanationOfSystem", ""),
            "stepByStepBulletPoints": fields.get("stepByStepBulletPoints", ""),
            "leftToRightFlowWithArrows": fields.get("leftToRightFlowWithArrows", ""),
            "aboutMeBulletPoints": fields.get("aboutMeBulletPoints", ""),
        },
    )
    proposal_url = google_client.doc_url(proposal_id)

    logger.info("upwork: copying script doc from template %s", config.SCRIPT_TEMPLATE_ID)
    script_id = google_client.copy_doc(config.SCRIPT_TEMPLATE_ID, f"[Automation] Upwork sales script for {title}")
    google_client.share_doc(script_id, role="writer")
    google_client.fill_doc(
        script_id,
        {
            "shortSummary": fields.get("briefExplanationOfSystem", ""),
            "stepByStepBuilding": fields.get("stepByStepBulletPoints", ""),
            "mermaidCode": diagram,
        },
    )
    script_url = google_client.doc_url(script_id)

    logger.info("upwork: appending tracking row to sheet %s", config.TRACKING_SHEET_ID)
    google_client.append_row(
        config.TRACKING_SHEET_ID,
        config.TRACKING_SHEET_RANGE,
        [
            datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M"),
            title,
            job_description,
            fields.get("briefExplanationOfSystem", ""),
            "",
            "",
            proposal_url,
            script_url,
            "",
        ],
    )

    final_body = application_body.replace("$$$", proposal_url)
    return {
        "application_body": final_body,
        "proposal_url": proposal_url,
        "script_url": script_url,
    }
