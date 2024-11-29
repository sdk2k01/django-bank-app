from django.db import models
from django.db.models.fields.related import ForeignKey

from .customers import Customer


# Products (Accounts) abstract base class
class Products(models.Model):
    ac_holder = ForeignKey(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:  # type: ignore
        abstract = True


# Account Types
# Savings Account
class SavingsAccount(Products):
    def gen_ac_no():
        last_ac = SavingsAccount.objects.last()
        if last_ac:
            return "SB" + str(int(last_ac.ac_no[2::]) + 1).zfill(18)
        return "SB" + "1".zfill(18)

    ac_no = models.CharField(
        max_length=20, primary_key=True, default=gen_ac_no, editable=False
    )


# Current Account
class CurrentAccount(Products):
    def gen_ac_no():
        last_ac = CurrentAccount.objects.last()
        if last_ac:
            return "CA" + str(int(last_ac.ac_no[2::]) + 1).zfill(18)
        return "CA" + "1".zfill(18)

    ac_no = models.CharField(
        max_length=20, primary_key=True, default=gen_ac_no, editable=False
    )
