from django.contrib import admin

# Register your models here.
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Customer Information", {"fields": ["pan", "ph_no"]}),
    ]
    list_display = ["name", "cif", "ph_no"]


admin.site.register(Customer, CustomerAdmin)


class BaseProductAdmin(admin.ModelAdmin):
    list_display = ["ac_no", "ac_type", "ac_holder"]
    readonly_fields = ["ac_type"]

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(SavingsAccount)
class SavingsAccountAdmin(BaseProductAdmin):
    pass


@admin.register(CurrentAccount)
class CurrentAccountAdmin(BaseProductAdmin):
    pass


@admin.register(CashCreditAccount)
class CashCreditAccountAdmin(BaseProductAdmin):
    pass


class BaseCardsAdmin(admin.ModelAdmin):
    readonly_fields = ["card_type"]

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(CreditCard)
class CreditCardAdmin(BaseCardsAdmin):
    pass


@admin.register(DebitCard)
class DebitCardAdmin(BaseCardsAdmin):
    pass


@admin.register(ATMCard)
class ATMCardAdmin(BaseCardsAdmin):
    pass


@admin.register(PrepaidCard)
class PrepaidCardAdmin(BaseCardsAdmin):
    pass
