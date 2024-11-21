from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from factory import Faker

from bank.factories import CustomerFactory
from bank.models import CurrentAccount, Customer, SavingsAccount


class TestAccountCreation(TestCase):
    """
    Unit Test Case dealing with Account Creation.
    """

    def setUp(self) -> None:
        customer = CustomerFactory()
        password = Faker("password")
        self.user = User.objects.create(username=customer.pan, password=password)
        self.customer = Customer.objects.create(
            user=self.user,
            pan=customer.pan,
            name=customer.name,
            ph_no=customer.ph_no,
        )

    def test_create_savings_account(self):
        """
        Test Happy Path for savings account creation.
        """
        sba = SavingsAccount.objects.create(ac_holder=self.customer)
        self.assertEqual(sba.ac_type, "SB")
        self.assertEqual(sba.ac_holder, self.customer)
        retrieved_sba = SavingsAccount.objects.get(ac_no=sba.ac_no)
        self.assertEqual(retrieved_sba.ac_type, sba.ac_type)
        self.assertEqual(retrieved_sba.ac_holder, sba.ac_holder)
        self.assertEqual(retrieved_sba.ac_holder.user, sba.ac_holder.user)
        self.assertEqual(retrieved_sba.created, sba.created)

    def test_create_current_account(self):
        """
        Test Sad Path for current account creation.
        """
        ca = CurrentAccount.objects.create(ac_holder=self.customer)
        self.assertEqual(ca.ac_type, "CA")
        self.assertEqual(ca.ac_holder, self.customer)
        retrieved_ca = CurrentAccount.objects.get(ac_no=ca.ac_no)
        self.assertEqual(retrieved_ca.ac_type, ca.ac_type)
        self.assertEqual(retrieved_ca.ac_holder, ca.ac_holder)
        self.assertEqual(retrieved_ca.ac_holder.user, ca.ac_holder.user)
        self.assertEqual(retrieved_ca.created, ca.created)
