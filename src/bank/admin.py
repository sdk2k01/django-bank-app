from django.contrib import admin

# Register your models here.
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Linked User", {"fields": ["user"]}),
        ("Customer Information", {"fields": ["pan", "ph_no"]}),
    ]
    list_display = ["cif", "name", "ph_no", "created", "modified"]


admin.site.register(Customer, CustomerAdmin)


class BaseProductAdmin(admin.ModelAdmin):
    list_display = ["ac_no", "ac_type", "ac_holder", "created"]
    readonly_fields = ["ac_type"]

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(SavingsAccount)
class SavingsAccountAdmin(BaseProductAdmin):
    pass


@admin.register(CurrentAccount)
class CurrentAccountAdmin(BaseProductAdmin):
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


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = ["txn_no", "type", "amt_txned", "initiated", "ac_no"]
    readonly_fields = ["txn_no", "type", "amt_txned", "initiated", "ac_no"]
