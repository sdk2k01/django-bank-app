from django.contrib.auth.models import User
from django.db import models

from .utils import validate_digit_length


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer_profile"
    )
    cif = models.BigAutoField(primary_key=True)
    pan = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=20)
    ph_no = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_digit_length],
        default="0000000000",
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        # Prevent manual setting of immutable fields
        for field in ["cif", "created", "modified"]:
            if field in kwargs:
                raise TypeError(f"'{field}' cannot be manually set")
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        # return f"{self.cif} - {self.name}"
        return self.name
