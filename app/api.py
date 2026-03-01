"""Admin API: contacts, call/SMS history (Twilio), test call/SMS."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.config import settings
from app.contacts import load_contacts
from app.twilio_client import list_calls, list_messages, send_sms, create_call

router = APIRouter(prefix="/api", tags=["admin"])


# --- Response / request models ---


class ContactOut(BaseModel):
    id: int
    name: str
    phone: str


class TestCallRequest(BaseModel):
    to: str


class TestSmsRequest(BaseModel):
    to: str
    body: str = "Test message from admin dashboard"


# --- Endpoints ---


@router.get("/contacts", response_model=list[ContactOut])
def get_contacts():
    """List predefined contacts (phone numbers added to the directory)."""
    contacts = load_contacts()
    return [ContactOut(id=c.id, name=c.name, phone=c.phone) for c in contacts]


@router.get("/calls")
def get_calls(limit: int = 50):
    """List recent calls (from Twilio)."""
    try:
        return list_calls(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Twilio error: {e!s}") from e


@router.get("/messages")
def get_messages(limit: int = 50):
    """List recent SMS (from Twilio)."""
    try:
        return list_messages(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Twilio error: {e!s}") from e


def _get_base_url(request: Request) -> str:
    """Use BASE_URL from env, or derive from request (X-Forwarded-* or Host) when behind ngrok."""
    base = (settings.base_url or "").strip().rstrip("/")
    if base:
        return base
    # Derive from request (ngrok adds X-Forwarded-Host, X-Forwarded-Proto)
    host = (request.headers.get("x-forwarded-host") or request.headers.get("host") or "").split(",")[0].strip()
    proto = (request.headers.get("x-forwarded-proto") or "https").split(",")[0].strip()
    if host:
        return f"{proto}://{host}"
    return ""


@router.post("/test/call")
def test_call(request: Request, req: TestCallRequest):
    """Start a test call: Twilio calls `to`; when they answer, they hear the directory menu."""
    base = _get_base_url(request)
    if not base:
        raise HTTPException(
            status_code=400,
            detail="Could not determine base URL. Set BASE_URL in .env (e.g. https://xxx.ngrok.io) or access the admin via your ngrok URL.",
        )
    voice_url = f"{base}/webhooks/voice"
    try:
        result = create_call(to=req.to, url=voice_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Twilio error: {e!s}") from e


@router.post("/test/sms")
def test_sms(req: TestSmsRequest):
    """Send a test SMS from the Twilio number to `to`."""
    try:
        send_sms(to=req.to, body=req.body)
        return {"ok": True, "to": req.to}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Twilio error: {e!s}") from e
