from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView

from bank.models import CreditCard, CurrentAccount, Customer, DebitCard, SavingsAccount


# Base Card Mixins & Forms
class BaseCardMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_type"] = self.model.__name__
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
        context["card_type"] = self.request.path.rstrip("/").rsplit("/", maxsplit=2)[-2]
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


# Credit Card Actions
class CreditCardListView(
    LoginRequiredMixin, BaseCardMixin, BaseCardListMixin, ListView
):
    model = CreditCard
    redirect_field_name = "/cards/cc/"


class CreditCardDetailView(
    LoginRequiredMixin, BaseCardMixin, BaseCardDetailMixin, DetailView
):
    model = CreditCard
    redirect_field_name = "/cards/cc/"


class CreditCardCreationView(LoginRequiredMixin, BaseCardCreationMixin, CreateView):
    model = CreditCard
    form_class = CreditCardCreationForm
    redirect_field_name = "/cards/cc/create/"
    success_url = "/cards/cc/"


# Debit Card Actions
class DebitCardListView(LoginRequiredMixin, BaseCardMixin, BaseCardListMixin, ListView):
    model = DebitCard
    redirect_field_name = "/cards/dc/"


class DebitCardDetailView(
    LoginRequiredMixin, BaseCardMixin, BaseCardDetailMixin, DetailView
):
    model = DebitCard
    redirect_field_name = "/cards/dc/"


class DebitCardCreationView(LoginRequiredMixin, BaseCardCreationMixin, CreateView):
    model = DebitCard
    form_class = DebitCardCreationForm
    redirect_field_name = "/cards/dc/create/"
    success_url = "/cards/dc/"
