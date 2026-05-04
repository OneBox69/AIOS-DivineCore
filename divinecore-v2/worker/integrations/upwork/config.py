"""Constants for the Upwork integration. Single place to change template/sheet IDs."""

from settings import settings

PROPOSAL_TEMPLATE_ID = settings.UPWORK_PROPOSAL_TEMPLATE_ID
SCRIPT_TEMPLATE_ID = settings.UPWORK_SCRIPT_TEMPLATE_ID
TRACKING_SHEET_ID = settings.UPWORK_TRACKING_SHEET_ID

PROPOSAL_PLACEHOLDERS = (
    "titleOfSystem",
    "briefExplanationOfSystem",
    "stepByStepBulletPoints",
    "leftToRightFlowWithArrows",
    "aboutMeBulletPoints",
)

SCRIPT_PLACEHOLDERS = (
    "shortSummary",
    "stepByStepBuilding",
    "mermaidCode",
)

TRACKING_SHEET_RANGE = "Sheet1!A:Z"
