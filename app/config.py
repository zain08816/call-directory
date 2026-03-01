"""Configuration via environment variables (pydantic-settings)."""
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_contacts_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "contacts.json"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""
    allowed_phone_numbers: str = ""
    contacts_path: Path = _default_contacts_path()
    base_url: str = ""  # e.g. https://xxx.ngrok.io for test call TwiML URL
    admin_dev_proxy: bool = False  # when True, proxy /admin to Vite on 5173 (single address)

    @field_validator("allowed_phone_numbers", mode="before")
    @classmethod
    def parse_allowed_numbers(cls, v: object) -> str:
        if isinstance(v, list):
            return ",".join(str(x) for x in v)
        return str(v) if v is not None else ""

    def get_allowed_list(self) -> list[str]:
        """Return normalized E.164-style list of allowed numbers (strip, no empty)."""
        if not self.allowed_phone_numbers:
            return []
        return [
            n.strip()
            for n in self.allowed_phone_numbers.split(",")
            if n.strip()
        ]


settings = Settings()


def is_allowed(phone: str) -> bool:
    """Check if phone (From) is in the allowlist, or is our Twilio number (for test/outbound calls)."""
    if not phone:
        return False
    p = phone.strip()
    # Our Twilio number is always allowed (e.g. when we place a test call, From = our number)
    if settings.twilio_phone_number and p == settings.twilio_phone_number.strip():
        return True
    allowed = settings.get_allowed_list()
    if not allowed:
        return False
    return p in allowed
