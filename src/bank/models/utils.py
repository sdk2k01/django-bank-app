from django.core.exceptions import ValidationError
from django.utils import timezone


# Helper Functions
def validate_phone_no(phone):
    if not (phone.isdigit() and len(phone) == 10):
        raise ValidationError(
            "%(phone)s must be 10 digits",
            params={"phone": phone},
        )


def validate_pan_no(pan):
    if not (
        pan[:5:].isalpha()
        and pan[5:-1:].isdigit()
        and pan[-1].isalpha()
        and pan[3] == "P"
    ):
        raise ValidationError(
            "Invalid PAN Number: %(pan)s",
            params={"pan": pan},
        )


def validate_card_no(card):
    if not (card.isdigit() and len(card) == 16):
        raise ValidationError(
            "%(card)s must be 16 digits",
            params={"card": card},
        )


def get_card_expiry():
    """
    Set default expiry date as 10 years from now.
    """
    return timezone.now() + timezone.timedelta(days=(365 * 10))
