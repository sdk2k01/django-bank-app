from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import generics

from bank.models import CreditCard, CurrentAccount, Customer, DebitCard, SavingsAccount
from bank.permissions import *
from bank.serializers import CreditCardSerializer, DebitCardSerializer


# Cards Accounts
class CardsCreationView(generics.ListCreateAPIView):
    """
    View for creating and viewing cards from user accounts.
    """

    permission_classes = [UserIsCardHolder]

    def get_card_type(self):
        return self.request.query_params.get("card_type", "cc")

    def get_customer(self):
        return generics.get_object_or_404(Customer, user=self.request.user)

    def get_customer_accounts(self):
        customer = self.get_customer()
        accounts = {
            "sb": [
                account.ac_no
                for account in SavingsAccount.objects.filter(ac_holder=customer)
            ],  # Savings accounts
            "ca": [
                account.ac_no
                for account in CurrentAccount.objects.filter(ac_holder=customer)
            ],  # Current accounts
        }
        return accounts

    def get_serializer_class(self):
        if self.get_card_type() == "cc":
            return CreditCardSerializer
        return DebitCardSerializer

    def get_queryset(self):
        ac_no = self.kwargs.get("ac_no")
        if ac_no is None:
            accounts = self.get_customer_accounts()
            accounts_list = accounts["sb"] + accounts["ca"]

            if self.get_card_type() == "cc":
                return CreditCard.objects.filter(ac_no__in=accounts_list)
            return DebitCard.objects.filter(ac_no__in=accounts_list)
        else:
            if self.get_card_type() == "cc":
                return CreditCard.objects.filter(ac_no=ac_no)
            return DebitCard.objects.filter(ac_no=ac_no)

    def perform_create(self, serializer):
        ac_no = self.kwargs.get("ac_no")
        serializer.save(ac_no=ac_no)


class AccountCardsView(generics.RetrieveUpdateAPIView):
    """
    Get details of cards and update partially belonging to a particular account.
    """

    permission_classes = [UserHoldsAccount]
    lookup_field = "card_no"

    def get_card_type(self):
        return self.request.query_params.get("card_type", "cc")

    def get_customer(self):
        return generics.get_object_or_404(Customer, user=self.request.user)

    def get_customer_accounts(self):
        customer = self.get_customer()
        accounts = [
            account.ac_no
            for account in SavingsAccount.objects.filter(ac_holder=customer)
        ] + [
            account.ac_no
            for account in CurrentAccount.objects.filter(ac_holder=customer)
        ]
        return accounts

    def get_serializer_class(self):
        if self.get_card_type() == "cc":
            return CreditCardSerializer
        return DebitCardSerializer

    def get_queryset(self):
        card_no = self.kwargs.get("card_no")
        if self.get_card_type() == "cc":
            return CreditCard.objects.filter(card_no=card_no)
        return DebitCard.objects.filter(card_no=card_no)


class ListCardsView(generics.ListAPIView):
    """
    For viewing all cards by type by admin.
    """

    permission_classes = [permissions.IsAdminUser]

    def get_card_type(self):
        return self.request.query_params.get("card_type", "cc")

    def get_serializer_class(self, *args, **kwargs):
        if self.get_card_type() == "cc":
            return CreditCardSerializer
        return DebitCardSerializer

    def get_queryset(self):
        if self.get_card_type() == "cc":
            return CreditCard.objects.all()
        return DebitCard.objects.all()
