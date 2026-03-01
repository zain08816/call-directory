"""Load predefined contacts from JSON."""
import json
from pathlib import Path

from app.config import settings


class Contact:
    def __init__(self, id: int, name: str, phone: str):
        self.id = id
        self.name = name
        self.phone = phone.strip()

    def __repr__(self) -> str:
        return f"Contact(id={self.id}, name={self.name!r}, phone={self.phone!r})"


def load_contacts(path: Path | None = None) -> list[Contact]:
    """Load contacts from JSON file. Returns list of Contact, 1-based index for menu."""
    p = path or settings.contacts_path
    if not p.exists():
        return []
    raw = json.loads(p.read_text(encoding="utf-8"))
    contacts = []
    for row in raw:
        contacts.append(
            Contact(
                id=int(row["id"]),
                name=str(row["name"]).strip(),
                phone=str(row["phone"]).strip(),
            )
        )
    return contacts


def get_contact_by_digit(digit: str, path: Path | None = None) -> Contact | None:
    """Get contact by menu digit (1-based). digit is '1', '2', ..."""
    contacts = load_contacts(path)
    try:
        idx = int(digit)
        if 1 <= idx <= len(contacts):
            return contacts[idx - 1]
    except ValueError:
        pass
    return None


def menu_text(contacts: list[Contact] | None = None) -> str:
    """Human-readable menu: Reply 1 for Mom, 2 for Dad, ..."""
    if contacts is None:
        contacts = load_contacts()
    if not contacts:
        return "No contacts configured."
    lines = [f"{c.id} {c.name}" for c in contacts]
    return "Reply with a number: " + ", ".join(lines)
