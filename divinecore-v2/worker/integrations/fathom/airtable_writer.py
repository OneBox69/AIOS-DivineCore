from datetime import datetime, timezone

from pyairtable import Api
from pyairtable.formulas import match

from settings import settings
from team import is_team_email, resolve_by_email

TRANSCRIPT_LIMIT = 90_000


def _client():
    api = Api(settings.AIRTABLE_API_KEY)
    return api.table(settings.AIRTABLE_BASE_ID, settings.AIRTABLE_MEETINGS_TABLE)


def _resolve_owner(payload: dict) -> str:
    recorded_by = payload.get("recorded_by") or {}
    email = recorded_by.get("email") if isinstance(recorded_by, dict) else None
    member = resolve_by_email(email) if email else None
    return member["name"] if member else "unknown"


def _attendee_emails(payload: dict) -> list[str]:
    invitees = payload.get("calendar_invitees") or []
    return [i.get("email", "").lower() for i in invitees if i.get("email")]


def _split_attendees(payload: dict) -> tuple[str, str]:
    emails = _attendee_emails(payload)
    internal = [e for e in emails if is_team_email(e)]
    external = [e for e in emails if not is_team_email(e)]
    return ", ".join(internal + external), ", ".join(external)


def _truncate(text: str | None) -> str:
    if not text:
        return ""
    if len(text) <= TRANSCRIPT_LIMIT:
        return text
    return text[:TRANSCRIPT_LIMIT] + "\n\n[truncated — see Transcript URL for full version]"


def _duration_minutes(payload: dict) -> int:
    start = payload.get("recording_start_time")
    end = payload.get("recording_end_time")
    if not (start and end):
        return 0
    try:
        s = datetime.fromisoformat(start.replace("Z", "+00:00"))
        e = datetime.fromisoformat(end.replace("Z", "+00:00"))
        return max(0, int((e - s).total_seconds() // 60))
    except (ValueError, AttributeError):
        return 0


def _row(payload: dict, category: str) -> dict:
    attendees, external = _split_attendees(payload)
    return {
        "Meeting ID": payload.get("recording_id"),
        "Title": payload.get("meeting_title") or payload.get("title", ""),
        "Date": payload.get("recording_start_time") or payload.get("scheduled_start_time"),
        "Duration (min)": _duration_minutes(payload),
        "Owner": _resolve_owner(payload),
        "Attendees": attendees,
        "External Attendees": external,
        "Category": category,
        "Summary": payload.get("default_summary", ""),
        "Transcript": _truncate(payload.get("transcript", "")),
        "Transcript URL": payload.get("share_url") or payload.get("url", ""),
        "Recording URL": payload.get("url", ""),
        "Processed At": datetime.now(timezone.utc).isoformat(),
    }


def upsert(payload: dict, category: str) -> dict:
    table = _client()
    meeting_id = payload.get("recording_id")
    fields = _row(payload, category)
    existing = table.first(formula=match({"Meeting ID": meeting_id}))
    if existing:
        return table.update(existing["id"], fields)
    return table.create(fields)
