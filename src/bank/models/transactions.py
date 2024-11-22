from django.db import models


class Transaction(models.Model):
    """
    Class representing all types of transactions.
    """

    DEBIT = "DR"
    CREDIT = "CR"
    TXN_CHOICES = (
        (DEBIT, "Debited"),
        (CREDIT, "Credited"),
    )
    txn_no = models.BigAutoField(primary_key=True)
    initiated = models.DateTimeField(auto_now_add=True)
    amt_txned = models.PositiveIntegerField()
    type = models.CharField(max_length=2, choices=TXN_CHOICES, null=False)
    ac_no = models.CharField(max_length=20)
