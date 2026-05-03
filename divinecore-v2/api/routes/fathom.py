import hashlib
import hmac
import json

from celery import Celery
from fastapi import APIRouter, Header, HTTPException, Request

from settings import settings

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

_celery = Celery("api", broker=settings.REDIS_URL, backend=settings.REDIS_URL)


def _verify(body: bytes, signature: str | None) -> bool:
    if not settings.FATHOM_WEBHOOK_SECRET:
        return False
    if not signature:
        return False
    expected = hmac.new(
        settings.FATHOM_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()
    provided = signature.split("=", 1)[-1].strip()
    return hmac.compare_digest(expected, provided)


@router.post("/fathom")
async def fathom_webhook(
    request: Request,
    x_fathom_signature: str | None = Header(default=None),
):
    body = await request.body()
    if not _verify(body, x_fathom_signature):
        raise HTTPException(status_code=401, detail="invalid signature")

    payload = json.loads(body)
    _celery.send_task("tasks.process_fathom_recording", args=[payload])
    return {"received": True, "meeting_id": payload.get("recording_id") or payload.get("id")}
