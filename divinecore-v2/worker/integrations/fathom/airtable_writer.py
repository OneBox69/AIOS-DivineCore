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
    recorder = (payload.get("recorder") or {}).get("email") or payload.get("owner_email")
    member = resolve_by_email(recorder) if recorder else None
    return member["name"] if member else "unknown"


def _split_attendees(payload: dict) -> tuple[str, str]:
    emails = [a.get("email", "") for a in payload.get("attendees") or [] if a.get("email")]
    internal = [e for e in emails if is_team_email(e)]
    external = [e for e in emails if not is_team_email(e)]
    return ", ".join(internal + external), ", ".join(external)


def _truncate(text: str | None) -> str:
    if not text:
        return ""
    if len(text) <= TRANSCRIPT_LIMIT:
        return text
    return text[:TRANSCRIPT_LIMIT] + "\n\n[truncated — see Transcript URL for full version]"


def _row(payload: dict, category: str) -> dict:
    attendees, external = _split_attendees(payload)
    return {
        "Meeting ID": payload.get("recording_id") or payload.get("id"),
        "Title": payload.get("title", ""),
        "Date": payload.get("started_at") or payload.get("recorded_at"),
        "Duration (min)": payload.get("duration_minutes") or 0,
        "Owner": _resolve_owner(payload),
        "Attendees": attendees,
        "External Attendees": external,
        "Category": category,
        "Summary": payload.get("summary", ""),
        "Transcript": _truncate(payload.get("transcript", "")),
        "Transcript URL": payload.get("share_url") or payload.get("recording_url", ""),
        "Recording URL": payload.get("recording_url", ""),
        "Processed At": datetime.now(timezone.utc).isoformat(),
    }


def upsert(payload: dict, category: str) -> dict:
    table = _client()
    meeting_id = payload.get("recording_id") or payload.get("id")
    fields = _row(payload, category)
    existing = table.first(formula=match({"Meeting ID": meeting_id}))
    if existing:
        return table.update(existing["id"], fields)
    return table.create(fields)
