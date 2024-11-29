import random

from faker import Faker

fake = Faker()

from unicodedata import numeric

from faker.providers import BaseProvider
from faker.providers.phone_number import Provider as PhProvider
from mypy.metastore import random_string


class CustomProvider(BaseProvider):
    def bank_ac_no(self, ac_type: str):
        ac_no = "".join([str(random.randint(0, 9)) for _ in range(18)])
        return ac_type + ac_no


class IndianPhoneNumberProvider(PhProvider):
    def indian_ph_no(self):
        return self.msisdn()[3::]


fake.add_provider(CustomProvider)
fake.add_provider(IndianPhoneNumberProvider)
