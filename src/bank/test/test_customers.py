from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from factory import Faker

from bank.factories import CustomerFactory
from bank.models import Customer


class TestRegisterUser(TestCase):
    """
    Unit Test Case dealing with user registration.
    """

    def test_register_user_happy_path(self):
        """
        Test whether user registration is properly implemented.
        """
        customer = CustomerFactory()
        password = Faker("password")
        user = User.objects.create(username=customer.pan, password=password)
        created_customer = Customer.objects.create(
            user=user,
            pan=customer.pan,
            name=customer.name,
            ph_no=customer.ph_no,
        )
        retrieved_customer = Customer.objects.get(pan=customer.pan)
        self.assertEqual(retrieved_customer.user, created_customer.user)
        self.assertEqual(retrieved_customer.cif, created_customer.cif)
        self.assertEqual(retrieved_customer.name, created_customer.name)
        self.assertEqual(retrieved_customer.ph_no, created_customer.ph_no)
