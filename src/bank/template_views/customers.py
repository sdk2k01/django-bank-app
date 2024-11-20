from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
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

    def get_object(self, queryset=None):
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


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
