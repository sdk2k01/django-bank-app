from django.contrib.auth.models import User
from rest_framework import serializers

from bank.models import (
    CreditCard,
    CurrentAccount,
    Customer,
    DebitCard,
    SavingsAccount,
    Transaction,
)


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ["cif", "pan", "name", "ph_no", "password"]
        read_only_fields = ("cif",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            username=validated_data["pan"], password=password
        )
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class SBAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccount
        fields = ["ac_no", "ac_type", "ac_holder", "created"]
        read_only_fields = ["ac_holder"]


class CurrentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAccount
        fields = ["ac_no", "ac_type", "ac_holder", "created"]
        read_only_fields = ["ac_holder"]


class DebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCard
        fields = ["card_no", "card_type", "ac_no", "issued", "expiry"]
        read_only_fields = ["card_no", "card_type", "ac_no", "issued", "expiry"]


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ["card_no", "card_type", "ac_no", "issued", "expiry"]
        read_only_fields = ["card_no", "card_type", "ac_no", "issued", "expiry"]


class TransactionSerializer(serializers.ModelSerializer):
    # type = serializers.SerializerMethodField(method_name='get_type')

    class Meta:
        model = Transaction
        fields = ["txn_no", "initiated", "amt_txned", "ac_no", "type"]

    # def get_type(self, obj):
    #     view_name = self.context["view"].__class__.__name__
    #     if view_name == "Deposit":
    #         return Transaction.CREDIT
    #     elif view_name == "Withdraw":
    #         return Transaction.DEBIT
