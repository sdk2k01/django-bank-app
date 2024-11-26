from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import generics

from bank.models import CurrentAccount, Customer, Products, SavingsAccount
from bank.permissions import *
from bank.serializers import CurrentAccountSerializer, SBAccountSerializer


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
