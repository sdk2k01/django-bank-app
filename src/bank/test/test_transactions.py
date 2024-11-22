from django.contrib.auth.models import User
from django.test import TestCase
from factory import Faker

from bank.factories import CustomerFactory
from bank.models import CurrentAccount, Customer, SavingsAccount, Transaction
from bank.providers import fake


class TestTransactionCreation(TestCase):
    """
    Unit Test Case dealing with creation of transactions.
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
        self.sba = SavingsAccount.objects.create(ac_holder=self.customer)
        self.ca = CurrentAccount.objects.create(ac_holder=self.customer)

    def test_create_deposit_sba(self):
        """
        Test creation of Deposit to Savings Bank Account.
        """
        ac_no = self.sba.ac_no
        type = "CR"
        amt_txned = fake.random_number(digits=6, fix_len=False)
        cr_sba = Transaction.objects.create(ac_no=ac_no, amt_txned=amt_txned, type=type)
        self.assertEqual(cr_sba.type, "CR")
        self.assertEqual(cr_sba.ac_no, self.sba.ac_no)
        self.assertEqual(cr_sba.amt_txned, amt_txned)
        retrieved_cr = Transaction.objects.get(txn_no=cr_sba.txn_no)
        self.assertEqual(cr_sba.initiated, retrieved_cr.initiated)
        self.assertEqual(cr_sba.amt_txned, retrieved_cr.amt_txned)
        self.assertEqual(cr_sba.type, retrieved_cr.type)
        self.assertEqual(cr_sba.ac_no, retrieved_cr.ac_no)

    def test_create_deposit_ca(self):
        """
        Test creation of Deposit to Current Account.
        """
        ac_no = self.ca.ac_no
        type = "CR"
        amt_txned = fake.random_number(digits=6, fix_len=False)
        cr_ca = Transaction.objects.create(ac_no=ac_no, amt_txned=amt_txned, type=type)
        self.assertEqual(cr_ca.type, "CR")
        self.assertEqual(cr_ca.ac_no, self.ca.ac_no)
        self.assertEqual(cr_ca.amt_txned, amt_txned)
        retrieved_cr = Transaction.objects.get(txn_no=cr_ca.txn_no)
        self.assertEqual(cr_ca.initiated, retrieved_cr.initiated)
        self.assertEqual(cr_ca.amt_txned, retrieved_cr.amt_txned)
        self.assertEqual(cr_ca.type, retrieved_cr.type)
        self.assertEqual(cr_ca.ac_no, retrieved_cr.ac_no)

    def test_create_withdraw_sba(self):
        """
        Test creation of Withdrawal against Savings Bank Account.
        """
        ac_no = self.sba.ac_no
        type = "DR"
        amt_txned = fake.random_number(digits=6, fix_len=False)
        dr_sba = Transaction.objects.create(ac_no=ac_no, amt_txned=amt_txned, type=type)
        self.assertEqual(dr_sba.type, "DR")
        self.assertEqual(dr_sba.ac_no, self.sba.ac_no)
        self.assertEqual(dr_sba.amt_txned, amt_txned)
        retrieved_dr = Transaction.objects.get(txn_no=dr_sba.txn_no)
        self.assertEqual(dr_sba.initiated, retrieved_dr.initiated)
        self.assertEqual(dr_sba.amt_txned, retrieved_dr.amt_txned)
        self.assertEqual(dr_sba.type, retrieved_dr.type)
        self.assertEqual(dr_sba.ac_no, retrieved_dr.ac_no)

    def test_create_withdraw_ca(self):
        """
        Test creation of Withdrawal against Current Account.
        """
        ac_no = self.ca.ac_no
        type = "DR"
        amt_txned = fake.random_number(digits=6, fix_len=False)
        dr_ca = Transaction.objects.create(ac_no=ac_no, amt_txned=amt_txned, type=type)
        self.assertEqual(dr_ca.type, "DR")
        self.assertEqual(dr_ca.ac_no, self.ca.ac_no)
        self.assertEqual(dr_ca.amt_txned, amt_txned)
        retrieved_dr = Transaction.objects.get(txn_no=dr_ca.txn_no)
        self.assertEqual(dr_ca.initiated, retrieved_dr.initiated)
        self.assertEqual(dr_ca.amt_txned, retrieved_dr.amt_txned)
        self.assertEqual(dr_ca.type, retrieved_dr.type)
        self.assertEqual(dr_ca.ac_no, retrieved_dr.ac_no)
