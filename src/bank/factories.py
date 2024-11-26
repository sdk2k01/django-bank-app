import random

import factory

# from django.contrib.auth.models import User
from .models import Customer
from .providers import fake


class CustomerFactory(factory.Factory):
    class Meta:  # type: ignore
        model = Customer

    name = factory.Faker("name")
    ph_no = fake.indian_ph_no()
    pan = factory.LazyAttribute(
        lambda obj: f"PANP{obj.name.split()[1][0]}{random.randint(1000, 9999)}{chr(random.randint(65, 90))}"
    )
