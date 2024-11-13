from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import pre_save


# Helper Functions
def validate_digit_length(phone):
    if not (phone.isdigit() and len(phone) == 10):
        raise ValidationError(
            "%(phone)s must be 10 digits",
            params={"phone": phone},
        )


def validate_card_no(card):
    if not (card.isdigit() and len(card) == 16):
        raise ValidationError(
            "%(card)s must be 10 digits",
            params={"card": card},
        )


# Create your models here.
class Customer(models.Model):
    cif = models.BigAutoField(primary_key=True)
    pan = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=20)
    ph_no = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_digit_length],
        default="0000000000",
    )

    def __str__(self) -> str:
        return f"{self.cif} - {self.name}"


# Products (Accounts) abstract base class
class Products(models.Model):
    # Product Choices
    SAVINGS = "SB"
    CURRENT = "CA"
    CASH_CREDIT = "CC"
    PRODUCT_CHOICES = (
        (SAVINGS, "Savings Account"),
        (CURRENT, "Current Account"),
        (CASH_CREDIT, "Cash Credit Account"),
    )
    ac_no = models.CharField(max_length=20, primary_key=True, editable=False)
    ac_type = models.CharField(
        max_length=2, choices=PRODUCT_CHOICES, default=SAVINGS, editable=False
    )
    ac_holder = ForeignKey(Customer, on_delete=models.CASCADE)

    @classmethod
    def get_last_ac_no(cls, prefix):
        """Get the last account number for a given prefix. If not exists, create one."""
        last_account = (
            cls.objects.filter(ac_no__startswith=prefix).order_by("-ac_no").first()
        )

        if last_account:
            return int(last_account.ac_no[2:])
        return 0

    def save(self, *args, **kwargs):
        if not self.ac_type:
            # Set account_type based on the concrete class
            for choice in self.PRODUCT_CHOICES:
                if self.__class__.__name__.upper().startswith(choice[0]):
                    self.ac_type = choice[0]
                    break

        if not self.ac_no and self.ac_type:
            last_ac_no = self.__class__.get_last_ac_no(self.ac_type)
            new_ac_no = str(last_ac_no + 1).zfill(18)
            self.ac_no = f"{self.ac_type}{new_ac_no}"

        super().save(*args, **kwargs)

    class Meta:  # type: ignore
        abstract = True


# Account Types
# Savings Account
class SavingsAccount(Products):
    ac_type = Products.SAVINGS

    class Meta:  # type: ignore
        abstract = False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# Current Account
class CurrentAccount(Products):
    ac_type = Products.CURRENT

    class Meta:  # type: ignore
        abstract = False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# CC Account
class CashCreditAccount(Products):
    ac_type = Products.CASH_CREDIT

    class Meta:  # type: ignore
        abstract = False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# Cards abstract base class
class Cards(models.Model):
    # Card Type Choices
    DEBIT = "DR"
    CREDIT = "CR"
    ATM = "AC"
    PREPAID = "PP"
    CARD_CHOICES = (
        (DEBIT, "Debit Card"),
        (CREDIT, "Credit Card"),
        (ATM, "ATM Card"),
        (PREPAID, "Prepaid Card"),
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

    @classmethod
    def card_no_gen_helper(cls, prefix):
        """Get the last card number for a given prefix. If not exists, create one."""
        card_type_to_iin = {
            "DR": "1231",
            "CR": "1232",
            "AC": "1233",
            "PP": "1234",
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
            self.ATM: "1233",
            self.PREPAID: "1234",
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


# ATM Card
class ATMCard(Cards):
    card_type = Cards.ATM

    class Meta:  # type: ignore
        abstract = False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# Prepaid Card
class PrepaidCard(Cards):
    card_type = Cards.PREPAID

    class Meta:  # type: ignore
        abstract = False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
