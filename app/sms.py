"""SMS webhook: menu, connect session, relay user <-> contact, disconnect."""
from fastapi import APIRouter, Request, Form
from fastapi.responses import PlainTextResponse

from app.config import settings
from app.contacts import load_contacts, get_contact_by_digit, menu_text
from app.sms_sessions import (
    set_session,
    get_contact_for_user,
    get_user_for_contact,
    clear_user_session,
)
from app.twilio_client import send_sms
from app.config import is_allowed

router = APIRouter()

DISCONNECT_KEYWORDS = frozenset({"stop", "0", "disconnect", "end", "quit"})


def _normalize_body(body: str) -> str:
    return (body or "").strip()


@router.post("/sms")
async def sms_webhook(
    request: Request,
    From: str = Form(default=""),
    To: str = Form(default=""),
    Body: str = Form(default=""),
) -> PlainTextResponse:
    """Handle incoming SMS: allowlist, menu, connect, or relay."""
    from_num = From.strip()
    body = _normalize_body(Body)

    if not is_allowed(from_num):
        return PlainTextResponse("Unauthorized.", status_code=200)

    contacts = load_contacts()
    if not contacts:
        return PlainTextResponse("No contacts configured.")

    # Check if sender is a contact replying (we have a session contact_phone -> user_phone)
    user_for_contact = get_user_for_contact(from_num)
    if user_for_contact is not None:
        user_phone, contact_name = user_for_contact
        # Relay contact's message to the user
        send_sms(user_phone, f"{contact_name}: {body}")
        return PlainTextResponse("")  # No reply to contact needed

    # Sender is the user (allowlisted)
    session = get_contact_for_user(from_num)

    # Disconnect: clear session and show menu
    if body.lower() in DISCONNECT_KEYWORDS:
        clear_user_session(from_num)
        return PlainTextResponse(menu_text(contacts))

    # Active session: forward user message to contact
    if session is not None:
        contact_phone, _ = session
        send_sms(contact_phone, body)
        return PlainTextResponse("")

    # No session: treat as menu choice or show menu
    if body.isdigit() and len(body) == 1:
        contact = get_contact_by_digit(body)
        if contact:
            set_session(from_num, contact.phone, contact.name)
            return PlainTextResponse(
                f"Connected to {contact.name}. Send your message. Reply STOP to disconnect."
            )

    return PlainTextResponse(menu_text(contacts))
