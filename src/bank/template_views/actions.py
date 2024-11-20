from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from bank.models import CurrentAccount, Customer, SavingsAccount, Transaction


class UserTransactionsMixin:
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

    def get_queryset(self):
        customer_accounts = self.get_customer_accounts()
        return self.model.objects.filter(ac_no__in=customer_accounts)


class TransactionCreationForm(forms.ModelForm):
    class Meta:  # type: ignore
        model = Transaction
        fields = ["amt_txned", "ac_no"]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class DepositCreationView(CreateView):
    model = Transaction
    form_class = TransactionCreationForm
    template_name = "actions/deposit.html"
    success_url = "/transactions/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = Transaction.CREDIT
        return context

    def form_valid(self, form):
        form.instance.type = self.get_context_data()["type"]
        return super().form_valid(form)


class WithdrawCreationView(LoginRequiredMixin, UserTransactionsMixin, CreateView):
    model = Transaction
    form_class = TransactionCreationForm
    template_name = "actions/withdraw.html"
    success_url = "/transactions/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = Transaction.DEBIT
        context["customer_accounts"] = self.get_customer_accounts()
        return context

    def form_valid(self, form):
        form.instance.type = self.get_context_data()["type"]
        return super().form_valid(form)


class TransactionsListView(LoginRequiredMixin, UserTransactionsMixin, ListView):
    model = Transaction
    template_name = "actions/list.html"
    context_object_name = "transactions"


class TransactionDetailView(LoginRequiredMixin, UserTransactionsMixin, DetailView):
    model = Transaction
    template_name = "actions/detail.html"
    context_object_name = "transaction"
