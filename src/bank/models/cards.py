from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

from .utils import get_card_expiry, validate_card_no


# Cards abstract base class
class Cards(models.Model):
    # Card Type Choices
    DEBIT = "DC"
    CREDIT = "CC"
    CARD_CHOICES = (
        (DEBIT, "Debit Card"),
        (CREDIT, "Credit Card"),
    )
    card_no = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        validators=[validate_card_no],
        blank=True,
    )
    card_type = models.CharField(
        max_length=2, choices=CARD_CHOICES, default=DEBIT, editable=False
    )
    ac_no = models.CharField(max_length=20)
    issued = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(default=get_card_expiry)

    @classmethod
    def card_no_gen_helper(cls, prefix):
        """Get the last card number for a given prefix. If not exists, create one."""
        card_type_to_iin = {
            "DC": "1231",
            "CC": "1232",
        }
        last_account = (
            cls.objects.filter(card_no__startswith=card_type_to_iin[prefix])
            .order_by("-card_no")
            .first()
        )

        if last_account:
            return int(last_account.card_no[4:])
        return 0

    def save(self, *args, **kwargs):
        if not self.card_type:
            # Set account_type based on the concrete class
            for choice in self.CARD_CHOICES:
                if self.__class__.__name__.upper().startswith(choice[0]):
                    self.card_type = choice[0]
                    break

        card_type_to_iin = {
            self.DEBIT: "1231",
            self.CREDIT: "1232",
        }
        if not self.card_no and self.card_type:
            last_card_no = self.__class__.card_no_gen_helper(self.card_type)
            new_card_no = str(last_card_no + 1).zfill(12)
            self.card_no = f"{card_type_to_iin[self.card_type]}{new_card_no}"

        super().save(*args, **kwargs)

    class Meta:  # type: ignore
        abstract = True


# Card Types
# Debit Card
class DebitCard(Cards):
    card_type = Cards.DEBIT

    class Meta:  # type: ignore
        abstract = False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# Credit Card
class CreditCard(Cards):
    card_type = Cards.CREDIT

    class Meta:  # type: ignore
        abstract = False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
