from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
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
        created_customer = Customer(
            user=user,
            pan=customer.pan,
            name=customer.name,
            ph_no=customer.ph_no,
        )
        created_customer.full_clean()
        created_customer.save()
        retrieved_customer = Customer.objects.get(pan=customer.pan)
        self.assertEqual(retrieved_customer.user, created_customer.user)
        self.assertEqual(retrieved_customer.cif, created_customer.cif)
        self.assertEqual(retrieved_customer.name, created_customer.name)
        self.assertEqual(retrieved_customer.ph_no, created_customer.ph_no)

    def test_registration_with_invalid_ph_nos(self):
        """
        Test whether user registration with invalid phone no.s raises appropriate errors.
        """
        customer = CustomerFactory()
        password = Faker("password")
        user = User.objects.create(username=customer.pan, password=password)

        with self.assertRaises(ValidationError):
            invalid_cust_1 = Customer(
                user=user,
                pan=customer.pan,
                name=customer.name,
                ph_no="783503462",
            )
            invalid_cust_1.full_clean()
            invalid_cust_1.save()

        with self.assertRaises(ValidationError):
            invalid_cust_2 = Customer(
                user=user,
                pan=customer.pan,
                name=customer.name,
                ph_no="783503462A",
            )
            invalid_cust_2.full_clean()
            invalid_cust_2.save()

    def test_registration_with_invalid_pan_nos(self):
        """
        Test whether user registration with invalid pan no.s raises appropriate errors.
        """
        customer = CustomerFactory()
        password = Faker("password")
        user = User.objects.create(username=customer.pan, password=password)

        with self.assertRaises(ValidationError):
            invalid_cust_1 = Customer(
                user=user,
                pan=customer.ph_no,
                name=customer.name,
                ph_no=customer.ph_no,
            )
            invalid_cust_1.full_clean()
            invalid_cust_1.save()

        with self.assertRaises(ValidationError):
            invalid_cust_2 = Customer(
                user=user,
                pan="JMNPK97776",
                name=customer.name,
                ph_no=customer.ph_no,
            )
            invalid_cust_2.full_clean()
            invalid_cust_2.save()

        with self.assertRaises(ValidationError):
            invalid_cust_3 = Customer(
                user=user,
                pan="97838XDACK",
                name=customer.name,
                ph_no=customer.ph_no,
            )
            invalid_cust_3.full_clean()
            invalid_cust_3.save()

        with self.assertRaises(ValidationError):
            invalid_cust_4 = Customer(
                user=user,
                pan="JXKOK8797C",
                name=customer.name,
                ph_no=customer.ph_no,
            )
            invalid_cust_4.full_clean()
            invalid_cust_4.save()
