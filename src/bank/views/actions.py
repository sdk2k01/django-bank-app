from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import generics

from bank.models import CurrentAccount, Customer, SavingsAccount, Transaction
from bank.permissions import *
from bank.serializers import TransactionSerializer


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
