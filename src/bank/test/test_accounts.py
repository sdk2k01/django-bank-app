from django.contrib.auth.models import User
from django.test import TestCase
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

        account = SavingsAccount(ac_holder=self.customer)
        account.full_clean()
        account.save()
        self.assertEqual(account.ac_holder, self.customer)
        retrieved_account = SavingsAccount.objects.get(ac_no=account.ac_no)
        self.assertEqual(retrieved_account.ac_holder, account.ac_holder)
        self.assertEqual(retrieved_account.ac_holder.user, account.ac_holder.user)
        self.assertEqual(retrieved_account.created, account.created)

    def test_create_serial_savings_accounts(self):
        """
        Test whether creating serial savings accounts maintains the order of account no.s.
        """
        ac_1 = SavingsAccount.objects.create(ac_holder=self.customer)
        retrieved_ac = SavingsAccount.objects.get(ac_no=ac_1.ac_no)

        ac_2 = SavingsAccount(ac_holder=self.customer)
        ac_2.full_clean()

        self.assertEqual(int(ac_2.ac_no[2::]), int(retrieved_ac.ac_no[2::]) + 1)

    def test_create_current_account(self):
        """
        Test Sad Path for current account creation.
        """
        account = CurrentAccount(ac_holder=self.customer)
        account.full_clean()
        account.save()
        self.assertEqual(account.ac_holder, self.customer)
        retrieved_account = CurrentAccount.objects.get(ac_no=account.ac_no)
        self.assertEqual(retrieved_account.ac_holder, account.ac_holder)
        self.assertEqual(retrieved_account.ac_holder.user, account.ac_holder.user)
        self.assertEqual(retrieved_account.created, account.created)

    def test_create_serial_current_accounts(self):
        """
        Test whether creating serial current accounts maintains the order of account no.s.
        """
        ac_1 = CurrentAccount.objects.create(ac_holder=self.customer)
        retrieved_ac = CurrentAccount.objects.get(ac_no=ac_1.ac_no)

        ac_2 = CurrentAccount(ac_holder=self.customer)
        ac_2.full_clean()

        self.assertEqual(int(ac_2.ac_no[2::]), int(retrieved_ac.ac_no[2::]) + 1)

    def test_create_serial_accounts_random_order(self):
        """
        Test whether creating serial accounts of various types maintains order of ac no.s for given type.
        """
        sba_1 = SavingsAccount.objects.create(ac_holder=self.customer)
        ca_1 = CurrentAccount.objects.create(ac_holder=self.customer)

        retrieved_sba = SavingsAccount.objects.get(ac_no=sba_1.ac_no)
        retrieved_ca = CurrentAccount.objects.get(ac_no=ca_1.ac_no)

        sba_2 = SavingsAccount(ac_holder=self.customer)
        sba_2.full_clean()

        self.assertEqual(int(sba_2.ac_no[2::]), int(retrieved_sba.ac_no[2::]) + 1)

        ca_2 = CurrentAccount(ac_holder=self.customer)
        ca_2.full_clean()

        self.assertEqual(int(ca_2.ac_no[2::]), int(retrieved_ca.ac_no[2::]) + 1)
