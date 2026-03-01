"""Voice webhook: TwiML menu + Gather + Dial."""
from fastapi import APIRouter, Request, Form
from fastapi.responses import Response

from app.config import settings
from app.contacts import load_contacts, get_contact_by_digit
from app.config import is_allowed

router = APIRouter()


@router.post("/hello")
async def hello_webhook() -> Response:
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        "<Say>Hello from your call directory app. Your Twilio and ngrok setup is working.</Say>"
        "</Response>"
    )
    return Response(content=xml, media_type="application/xml")


# Pause lengths (seconds) for a less abrupt experience
_PAUSE_START = 1
_PAUSE_END = 1


def _twiml_reject() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?><Response>'
        f'<Pause length="{_PAUSE_START}"/>'
        "<Say>You are not authorized to use this service.</Say>"
        f'<Pause length="{_PAUSE_END}"/>'
        "<Hangup/></Response>"
    )


def _twiml_menu(base_url: str) -> str:
    contacts = load_contacts()
    if not contacts:
        return (
            '<?xml version="1.0" encoding="UTF-8"?><Response>'
            f'<Pause length="{_PAUSE_START}"/>'
            "<Say>No contacts configured.</Say>"
            f'<Pause length="{_PAUSE_END}"/>'
            "<Hangup/></Response>"
        )
    parts = [f"Press {c.id} for {c.name}" for c in contacts]
    say_text = ". ".join(parts)
    action = f"{base_url.rstrip('/')}/webhooks/voice?step=connect"
    return (
        '<?xml version="1.0" encoding="UTF-8"?><Response>'
        f'<Pause length="{_PAUSE_START}"/>'
        f"<Gather numDigits=\"1\" action=\"{action}\" method=\"POST\">"
        f"<Say>{say_text}</Say>"
        "</Gather>"
        "<Say>We did not receive any input. Goodbye.</Say>"
        f'<Pause length="{_PAUSE_END}"/>'
        "<Hangup/>"
        "</Response>"
    )


def _twiml_dial(contact_phone: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?><Response>'
        f"<Dial>{contact_phone}</Dial>"
        "<Say>The party did not answer. Goodbye.</Say>"
        f'<Pause length="{_PAUSE_END}"/>'
        "<Hangup/>"
        "</Response>"
    )


def _twiml_invalid_choice() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?><Response>'
        f'<Pause length="{_PAUSE_START}"/>'
        "<Say>Invalid option. Goodbye.</Say>"
        f'<Pause length="{_PAUSE_END}"/>'
        "<Hangup/></Response>"
    )


@router.post("/voice")
async def voice_webhook(
    request: Request,
    From: str = Form(default=""),
    Digits: str = Form(default=""),
) -> Response:
    """Handle incoming call: allowlist, then menu or Dial."""
    step = request.query_params.get("step", "")
    from_num = From
    if not is_allowed(from_num):
        return Response(content=_twiml_reject(), media_type="application/xml")

    base_url = str(request.base_url).rstrip("/")

    # Callback from Gather with digit
    if step == "connect" and Digits:
        contact = get_contact_by_digit(Digits.strip())
        if contact:
            return Response(
                content=_twiml_dial(contact.phone),
                media_type="application/xml",
            )
        return Response(
            content=_twiml_invalid_choice(),
            media_type="application/xml",
        )

    # Initial call: show menu
    return Response(
        content=_twiml_menu(base_url),
        media_type="application/xml",
    )
