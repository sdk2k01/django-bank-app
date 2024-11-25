from django.db import models

from .utils import get_card_expiry


# Cards abstract base class
class Cards(models.Model):
    ac_no = models.CharField(max_length=20)
    issued = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(default=get_card_expiry)

    class Meta:  # type: ignore
        abstract = True


# Card Types
# Debit Card
class DebitCard(Cards):
    def gen_card_no():
        last_card = DebitCard.objects.last()
        if last_card:
            return "1231" + str(int(last_card.card_no[4::]) + 1).zfill(12)
        return "1231" + "1".zfill(12)

    card_no = models.CharField(
        max_length=16,
        primary_key=True,
        default=gen_card_no,
        editable=False,
    )


# Credit Card
class CreditCard(Cards):
    def gen_card_no():
        last_card = CreditCard.objects.last()
        if last_card:
            return "1232" + str(int(last_card.card_no[4::]) + 1).zfill(12)
        return "1232" + "1".zfill(12)

    card_no = models.CharField(
        max_length=16,
        primary_key=True,
        default=gen_card_no,
        editable=False,
    )
