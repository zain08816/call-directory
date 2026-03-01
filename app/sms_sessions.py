"""In-memory session store: user_phone <-> contact_phone for SMS relay."""
from __future__ import annotations

# user_phone -> (contact_phone, contact_name) for sending user messages to contact
_user_to_contact: dict[str, tuple[str, str]] = {}
# contact_phone -> (user_phone, contact_name) for relaying contact replies to user
_contact_to_user: dict[str, tuple[str, str]] = {}


def set_session(user_phone: str, contact_phone: str, contact_name: str) -> None:
    """Record that user_phone is in a session with contact_phone (contact_name for messages)."""
    user_phone = user_phone.strip()
    contact_phone = contact_phone.strip()
    _user_to_contact[user_phone] = (contact_phone, contact_name)
    _contact_to_user[contact_phone] = (user_phone, contact_name)


def get_contact_for_user(user_phone: str) -> tuple[str, str] | None:
    """Return (contact_phone, contact_name) if user has an active session, else None."""
    return _user_to_contact.get(user_phone.strip())


def get_user_for_contact(contact_phone: str) -> tuple[str, str] | None:
    """Return (user_phone, contact_name) if this contact is in a session with a user, else None."""
    return _contact_to_user.get(contact_phone.strip())


def clear_user_session(user_phone: str) -> None:
    """Remove session for this user (and the reverse mapping)."""
    user_phone = user_phone.strip()
    entry = _user_to_contact.pop(user_phone, None)
    if entry:
        contact_phone, _ = entry
        _contact_to_user.pop(contact_phone, None)


def clear_contact_session(contact_phone: str) -> None:
    """Remove session for this contact (and the reverse mapping)."""
    contact_phone = contact_phone.strip()
    entry = _contact_to_user.pop(contact_phone, None)
    if entry:
        user_phone, _ = entry
        _user_to_contact.pop(user_phone, None)
