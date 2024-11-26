from django.contrib.auth.models import User
from django.test import TestCase
from factory import Faker

from bank.factories import CustomerFactory
from bank.models import CreditCard, CurrentAccount, Customer, DebitCard, SavingsAccount


class TestCardCreation(TestCase):
    """
    Unit Test Case dealing with card creation.
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

    def test_create_cc_sba(self):
        """
        Test creation of credit card from savings bank account.
        """
        cc_sb = CreditCard.objects.create(ac_no=self.sba.ac_no)
        self.assertEqual(cc_sb.card_type, "CC")
        self.assertEqual(cc_sb.ac_no, self.sba.ac_no)
        retrieved_cc = CreditCard.objects.get(card_no=cc_sb.card_no)
        self.assertEqual(cc_sb.ac_no, retrieved_cc.ac_no)
        self.assertEqual(cc_sb.card_type, retrieved_cc.card_type)
        self.assertEqual(cc_sb.issued, retrieved_cc.issued)
        self.assertEqual(cc_sb.expiry, retrieved_cc.expiry)

    def test_create_dc_sba(self):
        """
        Test creation of debit card from savings bank account.
        """
        dc_sb = DebitCard.objects.create(ac_no=self.sba.ac_no)
        self.assertEqual(dc_sb.card_type, "DC")
        self.assertEqual(dc_sb.ac_no, self.sba.ac_no)
        retrieved_dc = DebitCard.objects.get(card_no=dc_sb.card_no)
        self.assertEqual(dc_sb.ac_no, retrieved_dc.ac_no)
        self.assertEqual(dc_sb.card_type, retrieved_dc.card_type)
        self.assertEqual(dc_sb.issued, retrieved_dc.issued)

    def test_create_cc_ca(self):
        """
        Test creation of credit card from current account.
        """
        cc_ca = CreditCard.objects.create(ac_no=self.ca.ac_no)
        self.assertEqual(cc_ca.card_type, "CC")
        self.assertEqual(cc_ca.ac_no, self.ca.ac_no)
        retrieved_cc = CreditCard.objects.get(card_no=cc_ca.card_no)
        self.assertEqual(cc_ca.ac_no, retrieved_cc.ac_no)
        self.assertEqual(cc_ca.card_type, retrieved_cc.card_type)
        self.assertEqual(cc_ca.issued, retrieved_cc.issued)

    def test_create_dc_ca(self):
        """
        Test creation of debit card from current account.
        """
        dc_ca = DebitCard.objects.create(ac_no=self.ca.ac_no)
        self.assertEqual(dc_ca.card_type, "DC")
        self.assertEqual(dc_ca.ac_no, self.ca.ac_no)
        retrieved_dc = DebitCard.objects.get(card_no=dc_ca.card_no)
        self.assertEqual(dc_ca.ac_no, retrieved_dc.ac_no)
        self.assertEqual(dc_ca.card_type, retrieved_dc.card_type)
        self.assertEqual(dc_ca.issued, retrieved_dc.issued)
