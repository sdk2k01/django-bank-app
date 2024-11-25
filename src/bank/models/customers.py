from django.contrib.auth.models import User
from django.db import models

from .utils import validate_digit_length


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer_profile"
    )
    cif = models.BigAutoField(primary_key=True, editable=False)
    pan = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=20)
    ph_no = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_digit_length],
        default="0000000000",
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
