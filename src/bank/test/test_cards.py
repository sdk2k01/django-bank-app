from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from factory import Faker

from bank.factories import CustomerFactory
from bank.models import (
    CreditCard,
    CurrentAccount,
    Customer,
    DebitCard,
    SavingsAccount,
    cards,
)


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
        card = CreditCard(ac_no=self.sba.ac_no)
        card.full_clean()
        card.save()
        self.assertEqual(card.ac_no, self.sba.ac_no)
        retrieved_card = CreditCard.objects.get(card_no=card.card_no)
        self.assertEqual(card.ac_no, retrieved_card.ac_no)
        self.assertEqual(card.issued, retrieved_card.issued)
        self.assertEqual(card.expiry, retrieved_card.expiry)

    def test_create_dc_sba(self):
        """
        Test creation of debit card from savings bank account.
        """
        card = DebitCard(ac_no=self.sba.ac_no)
        card.full_clean()
        card.save()
        self.assertEqual(card.ac_no, self.sba.ac_no)
        retrieved_card = DebitCard.objects.get(card_no=card.card_no)
        self.assertEqual(card.ac_no, retrieved_card.ac_no)
        self.assertEqual(card.issued, retrieved_card.issued)

    def test_create_cc_ca(self):
        """
        Test creation of credit card from current account.
        """
        card = CreditCard(ac_no=self.ca.ac_no)
        card.full_clean()
        card.save()
        self.assertEqual(card.ac_no, self.ca.ac_no)
        retrieved_card = CreditCard.objects.get(card_no=card.card_no)
        self.assertEqual(card.ac_no, retrieved_card.ac_no)
        self.assertEqual(card.issued, retrieved_card.issued)

    def test_create_dc_ca(self):
        """
        Test creation of debit card from current account.
        """
        card = DebitCard(ac_no=self.ca.ac_no)
        card.full_clean()
        card.save()
        self.assertEqual(card.ac_no, self.ca.ac_no)
        retrieved_card = DebitCard.objects.get(card_no=card.card_no)
        self.assertEqual(card.ac_no, retrieved_card.ac_no)
        self.assertEqual(card.issued, retrieved_card.issued)

    def test_create_serial_cc(self):
        """
        Test whether creating credit cards serially maintains order of card no.s.
        """
        card_1 = CreditCard.objects.create(ac_no=self.ca.ac_no)
        retrieved_card = CreditCard.objects.get(card_no=card_1.card_no)

        card_2 = CreditCard(ac_no=self.sba.ac_no)
        card_2.full_clean()

        self.assertEqual(int(card_2.card_no[4::]), int(retrieved_card.ac_no[4::]) + 1)

    def test_create_serial_dc(self):
        """
        Test whether creating debit cards serially maintains order of card no.s.
        """
        card_1 = DebitCard.objects.create(ac_no=self.sba.ac_no)
        retrieved_card = DebitCard.objects.get(card_no=card_1.card_no)

        card_2 = DebitCard(ac_no=self.ca.ac_no)
        card_2.full_clean()

        self.assertEqual(int(card_2.card_no[4::]), int(retrieved_card.ac_no[4::]) + 1)

    def test_create_serial_cards_random_order(self):
        """
        Test whether creating cards of all types serially maintains order of card no.s.
        """
        dc_1 = DebitCard.objects.create(ac_no=self.sba.ac_no)
        cc_1 = CreditCard.objects.create(ac_no=self.ca.ac_no)

        retrieved_cc = CreditCard.objects.get(card_no=cc_1.card_no)
        cc_2 = CreditCard(ac_no=self.sba.ac_no)
        cc_2.full_clean()

        self.assertEqual(int(cc_2.card_no[4::]), int(retrieved_cc.card_no[4::]) + 1)

        retrieved_dc = DebitCard.objects.get(card_no=dc_1.card_no)
        dc_2 = DebitCard(ac_no=self.ca.ac_no)
        dc_2.full_clean()

        self.assertEqual(int(dc_2.card_no[4::]), int(retrieved_dc.card_no[4::]) + 1)
