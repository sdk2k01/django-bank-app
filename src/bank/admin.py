from django.contrib import admin

# Register your models here.
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Customer Information", {"fields": ["pan"]}),
    ]


admin.site.register(Customer, CustomerAdmin)
