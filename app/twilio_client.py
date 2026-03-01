"""Twilio client and helpers (send SMS, list calls/messages, create call)."""
from __future__ import annotations

from twilio.rest import Client

from app.config import settings

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        _client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token,
        )
    return _client


def send_sms(to: str, body: str, from_number: str | None = None) -> None:
    """Send an SMS from the configured Twilio number (or from_number) to `to`."""
    from_num = (from_number or settings.twilio_phone_number).strip()
    get_client().messages.create(to=to.strip(), from_=from_num, body=body)


def list_calls(limit: int = 50) -> list[dict]:
    """List recent calls for the account. Returns list of dicts with from, to, status, date_created, direction."""
    client = get_client()
    calls = client.calls.list(limit=limit)
    return [
        {
            "sid": c.sid,
            "from": getattr(c, "_from", None),
            "to": c.to,
            "status": c.status,
            "direction": c.direction,
            "date_created": c.date_created.isoformat() if c.date_created else None,
        }
        for c in calls
    ]


def list_messages(limit: int = 50) -> list[dict]:
    """List recent SMS for the account. Returns list of dicts with from, to, body, status, date_created, direction."""
    client = get_client()
    messages = client.messages.list(limit=limit)
    return [
        {
            "sid": m.sid,
            "from": m.from_,
            "to": m.to,
            "body": m.body or "",
            "status": m.status,
            "direction": m.direction,
            "date_created": m.date_created.isoformat() if m.date_created else None,
        }
        for m in messages
    ]


def create_call(to: str, url: str) -> dict:
    """Create an outbound call: from our Twilio number to `to`, TwiML at `url`. Returns call info dict."""
    client = get_client()
    call = client.calls.create(
        to=to.strip(),
        from_=settings.twilio_phone_number.strip(),
        url=url.strip(),
    )
    return {
        "sid": call.sid,
        "from": call.from_,
        "to": call.to,
        "status": call.status,
    }
