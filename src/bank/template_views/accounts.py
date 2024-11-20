from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from bank.models import CurrentAccount, Customer, SavingsAccount


# Base Account Mixins & Forms
class BaseAccountMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ac_type"] = self.model.__name__
        return context


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

    def form_valid(self, form):
        customer = self.request.user.customer_profile
        form.instance.ac_holder = customer
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_type"] = self.request.path.rstrip("/").rsplit("/", maxsplit=2)[
            -2
        ]
        return context


# Savings Account Views
class SavingsAccountListView(
    LoginRequiredMixin, BaseAccountMixin, BaseAccountListMixin, ListView
):
    model = SavingsAccount
    redirect_field_name = "/accounts/sb/"


class SavingsAccountDetailView(
    LoginRequiredMixin, BaseAccountMixin, BaseAccountDetailMixin, DetailView
):
    model = SavingsAccount
    redirect_field_name = "/accounts/sb/"


class SavingsAccountCreationView(
    LoginRequiredMixin, BaseAccountCreationMixin, CreateView
):
    model = SavingsAccount
    form_class = SavingsAccountCreationForm
    redirect_field_name = "/accounts/sb/create/"
    success_url = "/accounts/sb/"


# Current Account Views
class CurrentAccountListView(
    LoginRequiredMixin, BaseAccountMixin, BaseAccountListMixin, ListView
):
    model = CurrentAccount
    redirect_field_name = "/accounts/ca/"


class CurrentAccountDetailView(
    LoginRequiredMixin, BaseAccountMixin, BaseAccountDetailMixin, DetailView
):
    model = CurrentAccount
    redirect_field_name = "/accounts/ca/"


class CurrentAccountCreationView(
    LoginRequiredMixin, BaseAccountCreationMixin, CreateView
):
    model = CurrentAccount
    form_class = CurrentAccountCreationForm
    redirect_field_name = "/accounts/ca/create/"
    success_url = "/accounts/ca/"
