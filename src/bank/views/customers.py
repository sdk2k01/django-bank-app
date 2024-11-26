from django.db import transaction
from rest_framework import permissions
from rest_framework.viewsets import generics

from bank.models import Customer
from bank.permissions import *
from bank.serializers import CustomerSerializer


class CustomersView(generics.ListCreateAPIView):
    """
    Add a new customer or fetch list of all customers by admin.
    """

    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CustomerSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()


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
