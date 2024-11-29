from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView

from bank.models import CreditCard, CurrentAccount, Customer, DebitCard, SavingsAccount


# Base Card Mixins & Forms
class BaseCardMixin:
    def get_customer_accounts(self):
        customer = get_object_or_404(Customer, user=self.request.user)
        customer_accounts = []
        customer_accounts.extend(
            [sb.ac_no for sb in SavingsAccount.objects.filter(ac_holder=customer)]
        )
        customer_accounts.extend(
            [ca.ac_no for ca in CurrentAccount.objects.filter(ac_holder=customer)]
        )
        return customer_accounts


class BaseCardListMixin:
    template_name = "cards/list.html"
    context_object_name = "cards"

    def get_queryset(self):
        customer_accounts = self.get_customer_accounts()
        return self.model.objects.filter(ac_no__in=customer_accounts)


class BaseCardDetailMixin:
    template_name = "cards/detail.html"
    context_object_name = "card"

    def get_queryset(self):
        customer_accounts = self.get_customer_accounts()
        return self.model.objects.filter(ac_no__in=customer_accounts)


class CreditCardCreationForm(forms.ModelForm):
    class Meta:  # type: ignore
        model = CreditCard
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class DebitCardCreationForm(forms.ModelForm):
    class Meta:  # type: ignore
        model = DebitCard
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class BaseCardCreationMixin:
    template_name = "cards/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer_accounts"] = self.get_customer_accounts()
        return context

    def get_customer_accounts(self):
        customer = get_object_or_404(Customer, user=self.request.user)
        customer_accounts = []
        customer_accounts.extend(
            [sb.ac_no for sb in SavingsAccount.objects.filter(ac_holder=customer)]
        )
        customer_accounts.extend(
            [ca.ac_no for ca in CurrentAccount.objects.filter(ac_holder=customer)]
        )
        return customer_accounts

    def form_valid(self, form):
        account_number = self.request.POST.get("account_number")
        if not account_number:
            form.add_error(None, "Please select an account")
            return self.form_invalid(form)

        form.instance.ac_no = account_number
        return super().form_valid(form)


class CreditCardMixin:
    model = CreditCard
    extra_context = {"card_type": "Credit Card"}


class DebitCardMixin:
    model = DebitCard
    extra_context = {"card_type": "Debit Card"}


# Credit Card Actions
class CreditCardListView(
    LoginRequiredMixin, CreditCardMixin, BaseCardMixin, BaseCardListMixin, ListView
):
    redirect_field_name = "/cards/cc/"


class CreditCardDetailView(
    LoginRequiredMixin, CreditCardMixin, BaseCardMixin, BaseCardDetailMixin, DetailView
):
    redirect_field_name = "/cards/cc/"


class CreditCardCreationView(
    LoginRequiredMixin, CreditCardMixin, BaseCardCreationMixin, CreateView
):
    form_class = CreditCardCreationForm
    redirect_field_name = "/cards/cc/create/"
    success_url = "/cards/cc/"


# Debit Card Actions
class DebitCardListView(
    LoginRequiredMixin, DebitCardMixin, BaseCardMixin, BaseCardListMixin, ListView
):
    redirect_field_name = "/cards/dc/"


class DebitCardDetailView(
    LoginRequiredMixin, DebitCardMixin, BaseCardMixin, BaseCardDetailMixin, DetailView
):
    redirect_field_name = "/cards/dc/"


class DebitCardCreationView(
    LoginRequiredMixin, DebitCardMixin, BaseCardCreationMixin, CreateView
):
    form_class = DebitCardCreationForm
    redirect_field_name = "/cards/dc/create/"
    success_url = "/cards/dc/"
