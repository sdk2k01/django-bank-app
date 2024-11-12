from django.db import models


# Create your models here.
class Customer(models.Model):
    cif = models.BigAutoField(primary_key=True)
    pan = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=20)


class Products(models.Model):
    # Product Choices
    SAVINGS = "SB"
    CURRENT = "CA"
    CASH_CREDIT = "CC"
    PRODUCT_CHOICES = (
        (SAVINGS, "Savings"),
        (CURRENT, "Current Account"),
        (CASH_CREDIT, "Cash Credit Account"),
    )
    ac_type = models.CharField(
        max_length=2,
        choices=PRODUCT_CHOICES,
        default=SAVINGS,
    )

    class Meta:  # type: ignore
        abstract = True


class Cards(models.Model):
    # Card Type Choices
    card_type = models.CharField()

    class Meta:  # type: ignore
        abstract = True
