from pydantic import BaseModel, model_validator, Field, ValidationError
from enum import Enum
from datetime import datetime
from typing import Optional


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_values(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact must be verified")

        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError("Telepathic contact requires "
                             "at least 3 witnesses")

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals must include a message")

        return self


def main() -> None:
    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2026-04-11T12:00:00",
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli")

    print(
        "Alien Contact Log Validation\n"
        "======================================\n"
        "Valid contact report:\n"
        f"ID: {contact.contact_id}\n"
        f"Type: {contact.contact_type}\n"
        f"Location: {contact.location}\n"
        f"Signal: {contact.signal_strength}/10\n"
        f"Signal: {contact.signal_strength}/10\n"
        f"Duration: {contact.duration_minutes} minutes\n"
        f"Witnesses: {contact.witness_count}\n"
        f"Message: '{contact.message_received}'\n\n"
        "======================================")

    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp="2024-01-15T22:00:00",
            location="Mars Base",
            contact_type=ContactType.telepathic,
            signal_strength=6.0,
            duration_minutes=20,
            witness_count=1,
            message_received=None,
            is_verified=False
        )
    except ValidationError as e:
        print("Expected validation error:")
        error_info = e.errors()[0]
        print(error_info["ctx"]["error"])


if __name__ == "__main__":
    print()
    main()
    print()
