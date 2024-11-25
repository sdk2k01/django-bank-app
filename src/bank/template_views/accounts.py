from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from bank.models import CurrentAccount, SavingsAccount


# Base Account Mixins & Forms
class BaseAccountListMixin:
    template_name = "accounts/list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        return self.model.objects.filter(ac_holder=self.request.user.customer_profile)


class BaseAccountDetailMixin:
    template_name = "accounts/detail.html"
    context_object_name = "account"

    def get_queryset(self):
        return self.model.objects.filter(ac_holder=self.request.user.customer_profile)


class SavingsAccountMixin:
    model = SavingsAccount
    extra_context = {"account_type": "Savings Bank Account"}


class CurrentAccountMixin:
    model = CurrentAccount
    extra_context = {"account_type": "Current Account"}


class SavingsAccountCreationForm(forms.ModelForm):
    class Meta:  # type: ignore
        model = SavingsAccount
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class CurrentAccountCreationForm(forms.ModelForm):
    class Meta:  # type: ignore
        model = CurrentAccount
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class BaseAccountCreationMixin:
    template_name = "accounts/create.html"
    context_object_name = "customer"

    def form_valid(self, form):
        customer = self.request.user.customer_profile
        form.instance.ac_holder = customer
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer"] = self.request.user.customer_profile
        return context


# Savings Account Views
class SavingsAccountListView(
    LoginRequiredMixin, SavingsAccountMixin, BaseAccountListMixin, ListView
):
    redirect_field_name = "/accounts/sb/"


class SavingsAccountDetailView(
    LoginRequiredMixin, SavingsAccountMixin, BaseAccountDetailMixin, DetailView
):
    redirect_field_name = "/accounts/sb/"


class SavingsAccountCreationView(
    LoginRequiredMixin, SavingsAccountMixin, BaseAccountCreationMixin, CreateView
):
    form_class = SavingsAccountCreationForm
    redirect_field_name = "/accounts/sb/create/"
    success_url = "/accounts/sb/"


# Current Account Views
class CurrentAccountListView(
    LoginRequiredMixin, CurrentAccountMixin, BaseAccountListMixin, ListView
):
    redirect_field_name = "/accounts/ca/"


class CurrentAccountDetailView(
    LoginRequiredMixin, CurrentAccountMixin, BaseAccountDetailMixin, DetailView
):
    redirect_field_name = "/accounts/ca/"


class CurrentAccountCreationView(
    LoginRequiredMixin, CurrentAccountMixin, BaseAccountCreationMixin, CreateView
):
    form_class = CurrentAccountCreationForm
    redirect_field_name = "/accounts/ca/create/"
    success_url = "/accounts/ca/"
