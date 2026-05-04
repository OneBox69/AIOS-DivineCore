"""Google Docs/Drive/Sheets helpers. Auth via stored OAuth refresh token."""

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from settings import settings

SCOPES = (
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
)


def _credentials() -> Credentials:
    creds = Credentials(
        token=None,
        refresh_token=settings.GOOGLE_OAUTH_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
        client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
        scopes=list(SCOPES),
    )
    creds.refresh(Request())
    return creds


def _drive():
    return build("drive", "v3", credentials=_credentials(), cache_discovery=False)


def _docs():
    return build("docs", "v1", credentials=_credentials(), cache_discovery=False)


def _sheets():
    return build("sheets", "v4", credentials=_credentials(), cache_discovery=False)


def copy_doc(template_id: str, name: str) -> str:
    """Copy a Google Doc template, return the new document id."""
    result = _drive().files().copy(fileId=template_id, body={"name": name}).execute()
    return result["id"]


def share_doc(file_id: str, role: str = "reader") -> None:
    """Share `file_id` with anyone-with-link at the given role (reader|writer)."""
    _drive().permissions().create(
        fileId=file_id,
        body={"role": role, "type": "anyone"},
    ).execute()


def fill_doc(document_id: str, replacements: dict[str, str]) -> None:
    """batchUpdate replaceAllText for {{key}} -> value across the document."""
    requests = [
        {
            "replaceAllText": {
                "containsText": {"text": "{{" + key + "}}", "matchCase": True},
                "replaceText": value or "",
            }
        }
        for key, value in replacements.items()
    ]
    if not requests:
        return
    _docs().documents().batchUpdate(documentId=document_id, body={"requests": requests}).execute()


def append_row(spreadsheet_id: str, range_a1: str, row: list) -> None:
    """Append a single row to a sheet."""
    _sheets().spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_a1,
        valueInputOption="USER_ENTERED",
        body={"values": [row]},
    ).execute()


def doc_url(document_id: str) -> str:
    return f"https://docs.google.com/document/d/{document_id}/edit"
