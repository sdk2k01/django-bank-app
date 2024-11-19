from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from bank.models.customers import Customer


class CustomerListView(ListView):
    model = Customer
    template_name = "customers/list.html"
    context_object_name = "customers"


class CustomerDetailView(DetailView):
    model = Customer
    template_name = "customers/detail.html"
    context_object_name = "customer"


class CustomerCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:  # type: ignore
        model = Customer
        fields = ["pan", "name", "ph_no"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        return cleaned_data


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerCreationForm
    template_name = "customers/create.html"
    success_url = reverse_lazy("customer-list-template")

    @transaction.atomic  # Make user creation and customer creation atomic
    def form_valid(self, form):
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["pan"],  # Using PAN as username
                password=form.cleaned_data["password"],
            )

            customer = form.save(commit=False)
            customer.user = user
            customer.pan = form.cleaned_data["pan"]
            customer.save()

            return super().form_valid(form)
        return super().form_invalid(form)
