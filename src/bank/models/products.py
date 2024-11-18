from django.db import models
from django.db.models.fields.related import ForeignKey

from .customers import Customer


# Products (Accounts) abstract base class
class Products(models.Model):
    # Product Choices
    SAVINGS = "SB"
    CURRENT = "CA"
    PRODUCT_CHOICES = (
        (SAVINGS, "Savings Account"),
        (CURRENT, "Current Account"),
    )
    ac_no = models.CharField(max_length=20, primary_key=True, editable=False)
    ac_type = models.CharField(
        max_length=2, choices=PRODUCT_CHOICES, default=SAVINGS, editable=False
    )
    ac_holder = ForeignKey(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

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
