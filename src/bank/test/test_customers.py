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

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

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

    def test_registration_with_extra_cif(self):
        """
        Test whether creation of users with unallowed fields throws appropriate error.
        """
        customer = CustomerFactory()
        password = Faker("password")
        user = User.objects.create(username=customer.pan, password=password)
        cif = 69
        with self.assertRaises(TypeError):
            Customer.objects.create(
                user=user,
                cif=cif,
                pan=customer.pan,
                name=customer.name,
                ph_no=customer.ph_no,
            )

    def test_registration_with_extra_created(self):
        """
        Test whether creation of users with unallowed fields throws appropriate error.
        """
        customer = CustomerFactory()
        password = Faker("password")
        user = User.objects.create(username=customer.pan, password=password)
        created = timezone.now()
        with self.assertRaises(TypeError):
            Customer.objects.create(
                user=user,
                pan=customer.pan,
                name=customer.name,
                ph_no=customer.ph_no,
                created=created,
            )

    def test_registration_with_extra_modified(self):
        """
        Test whether creation of users with unallowed fields throws appropriate error.
        """
        customer = CustomerFactory()
        password = Faker("password")
        user = User.objects.create(username=customer.pan, password=password)
        modified = timezone.now()
        with self.assertRaises(TypeError):
            Customer.objects.create(
                user=user,
                pan=customer.pan,
                name=customer.name,
                ph_no=customer.ph_no,
                modified=modified,
            )

    def test_registration_with_extra_all(self):
        """
        Test whether creation of users with unallowed fields throws appropriate error.
        """
        customer = CustomerFactory()
        password = Faker("password")
        user = User.objects.create(username=customer.pan, password=password)
        cif = 69
        created = timezone.now()
        modified = timezone.now()
        with self.assertRaises(TypeError):
            Customer.objects.create(
                user=user,
                cif=cif,
                pan=customer.pan,
                name=customer.name,
                ph_no=customer.ph_no,
                created=created,
                modified=modified,
            )
