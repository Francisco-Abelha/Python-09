"""Exercise 1: Alien Contact Logs.

Master custom validation using @model_validator for complex business rules.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    """The medium through which alien contact was made."""

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """A validated report of a single alien contact event."""

    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
        """Cross-field rules that run after every field is validated."""
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )

        return self


def main() -> None:
    """Demonstrate a valid contact report and a failing validation."""
    print("Alien Contact Log Validation")
    print("=" * 38)

    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2024, 7, 4, 22, 15, 0),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )

    print("Valid contact report:")
    print(f"  ID: {contact.contact_id}")
    print(f"  Type: {contact.contact_type.value}")
    print(f"  Location: {contact.location}")
    print(f"  Signal: {contact.signal_strength}/10")
    print(f"  Duration: {contact.duration_minutes} minutes")
    print(f"  Witnesses: {contact.witness_count}")
    print(f"  Message: '{contact.message_received}'")

    print("=" * 38)

    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime(2024, 7, 5, 1, 0, 0),
            location="Roswell, New Mexico",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=5.0,
            duration_minutes=10,
            witness_count=1,  # invalid: telepathic needs >= 3 witnesses
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(f"  {error.errors()[0]['msg']}")


if __name__ == "__main__":
    main()
