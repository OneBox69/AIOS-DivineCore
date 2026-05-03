from datetime import datetime, timedelta, timezone

from pyairtable import Api

from settings import settings
from team import resolve_by_email, resolve_by_name

DEFAULT_DEADLINE_DAYS = 3

CHANNEL_BY_CATEGORY = {
    "client": "#sales-and-outreach",
    "sales": "#sales-and-outreach",
    "cofounder": "#pulse",
    "strategy": "#pulse",
    "other": "#pulse",
}


def _tasks_table():
    api = Api(settings.AIRTABLE_API_KEY)
    return api.table(settings.AIRTABLE_BASE_ID, settings.AIRTABLE_TASKS_TABLE)


def _resolve_assignee(raw: str) -> dict | None:
    if not raw:
        return None
    if "@" in raw:
        return resolve_by_email(raw)
    return resolve_by_name(raw)


def create_tasks_for_opted_in(payload: dict, meeting_record: dict) -> list[dict]:
    items = payload.get("action_items") or []
    if not items:
        return []

    table = _tasks_table()
    title = payload.get("title", "")
    date = payload.get("started_at", "")
    category = (meeting_record.get("fields") or {}).get("Category", "other")
    channel = CHANNEL_BY_CATEGORY.get(category, "#pulse")
    deadline = (datetime.now(timezone.utc) + timedelta(days=DEFAULT_DEADLINE_DAYS)).isoformat()

    created = []
    for item in items:
        assignee = _resolve_assignee(item.get("assignee", ""))
        if not assignee or not assignee.get("auto_pulse_tasks"):
            continue
        row = table.create({
            "Task": item.get("description", "").strip(),
            "Assignee": assignee["name"],
            "Channel": channel,
            "Status": "in-progress",
            "Priority": "medium",
            "Deadline": deadline,
            "Created By": "fathom",
            "Notes": f"From meeting: {title} ({date})",
        })
        created.append(row)
    return created
