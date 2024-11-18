from django.contrib.auth import authenticate, login

# from django.db import transaction
from django.shortcuts import render

# from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from bank.models import *
from bank.permissions import *
from bank.serializers import *


# Create your views here.
# Customer Actions
class RegisterCustomerView(generics.CreateAPIView):
    """
    Add a new customer.
    """

    permission_classes = [permissions.IsAdminUser]
    serializer_class = CustomerSerializer


class CustomerView(generics.RetrieveUpdateAPIView):
    """
    For fetching details of customer by self, or making partial updates.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsCustomer]
    http_method_names = ["get", "patch"]

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)

        # Make fields read-only if this is an update operation
        if self.request.method in ["PUT", "PATCH"]:
            serializer.fields["cif"].read_only = True
            serializer.fields["pan"].read_only = True

        return serializer


class CustomersView(generics.ListAPIView):
    """
    For fetching details of all customers by admin.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]


# Accounts Actions
class AccountCreationView(generics.ListCreateAPIView):
    """
    For creating new account by an existing customer or viewing list of accounts belonging to user.
    """

    permission_classes = [UserIsAcHolder]

    @action(detail=False, methods=["get"])
    def ac_types(self):
        """
        Endpoint to get available account types for the dropdown.
        """
        return Response(Products.PRODUCT_CHOICES)

    def get_account_type(self):
        return self.request.query_params.get("ac_type", "sb")

    def get_customer(self):
        return generics.get_object_or_404(Customer, user=self.request.user)

    def get_queryset(self):
        customer = self.get_customer()
        if self.get_account_type() == "sb":
            return SavingsAccount.objects.filter(ac_holder=customer)
        return CurrentAccount.objects.filter(ac_holder=customer)

    def get_serializer_class(self):
        if self.get_account_type() == "sb":
            return SBAccountSerializer
        return CurrentAccountSerializer

    def perform_create(self, serializer):
        ac_holder = self.get_customer()
        serializer.save(ac_holder=ac_holder)


class CustomerAccountsView(generics.RetrieveUpdateAPIView):
    """
    For viewing or updating partially (TBD) given user account.
    """

    permission_classes = [UserIsAcHolder]
    lookup_field = "ac_no"
    http_method_names = ["get", "patch"]

    def get_account_type(self):
        return self.request.query_params.get("ac_type", "sb")

    def get_customer(self):
        return generics.get_object_or_404(Customer, user=self.request.user)

    def get_serializer_class(self):
        if self.get_account_type() == "sb":
            return SBAccountSerializer
        return CurrentAccountSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)

        # Make fields read-only if this is an update operation
        if self.request.method in ["PUT", "PATCH"]:
            serializer.fields["ac_type"].read_only = True
            serializer.fields["ac_no"].read_only = True
            serializer.fields["created"].read_only = True

        return serializer

    def get_queryset(self):
        customer = self.get_customer()
        account_no = self.kwargs.get("ac_no")

        if self.get_account_type() == "sb":
            return SavingsAccount.objects.filter(ac_holder=customer)
        return CurrentAccount.objects.filter(ac_holder=customer)


class ListAccountsView(generics.ListAPIView):
    """
    For viewing list of all accounts by admin.
    """

    permission_classes = [permissions.IsAdminUser]

    def get_account_type(self):
        return self.request.query_params.get("ac_type", "sb")

    def get_serializer_class(self):
        if self.get_account_type() == "sb":
            return SBAccountSerializer
        return CurrentAccountSerializer

    def get_queryset(self):
        if self.get_account_type() == "sb":
            return SavingsAccount.objects.all()
        return CurrentAccount.objects.all()


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


# Banking Actions
class Deposit(generics.CreateAPIView):
    """
    Deposit money to an account.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        serializer.save(type=Transaction.CREDIT)


class Withdraw(generics.CreateAPIView):
    """
    Check balance or withdraw funds from account.
    """

    permission_classes = [UserIsCardHolder]
    serializer_class = TransactionSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.fields["type"].read_only = True
        return serializer

    def perform_create(self, serializer):
        serializer.save(type=Transaction.DEBIT)


class UserTransactions(generics.ListAPIView):
    """
    Display list of all transactions made by user.
    """

    permission_classes = [UserHoldsAccount]
    serializer_class = TransactionSerializer

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

    def get_queryset(self):
        customer_accounts = self.get_customer_accounts()
        return Transaction.objects.filter(ac_no__in=customer_accounts)


class ListTransactions(generics.ListAPIView):
    """
    Display list of all transactions (for admin only).
    """

    permission_classes = [permissions.IsAdminUser]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetails(generics.RetrieveAPIView):
    """
    Retrieve transaction details from account.
    """

    permission_classes = [UserHoldsAccount]
    serializer_class = TransactionSerializer

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

    def get_queryset(self):
        customer_accounts = self.get_customer_accounts()
        return Transaction.objects.filter(ac_no__in=customer_accounts)


# TBD (When implementing more complex structure)
# class BankStatement(generics.RetrieveAPIView):
#     """
#     Check or download bank statements.
#     """
#     def get(self, request, format=None):
#         return Response(None)


# class CloseAccount(generics.DestroyAPIView):
#     """
#     Close a bank account.
#     """
#     def delete(self, request, *args, **kwargs):
#         return Response(None)
