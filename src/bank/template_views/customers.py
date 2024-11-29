from webbrowser import get

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from bank.models.customers import Customer


# Create a base mixin for admin-only access
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            print(self.get_login_url())
            messages.error(
                self.request, "You don't have permission to access this page."
            )
            return HttpResponseForbidden(
                "403 Forbidden: You don't have permission to access this page."
            )
        return redirect(f"/{self.get_login_url()}?next={self.request.path}")


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy("login"))

        if request.user.is_staff or request.user.is_superuser:
            return reverse_lazy("customers-list")  # URL name for "customers/"
        else:
            return reverse_lazy("customer-details")


class CustomerListView(AdminRequiredMixin, ListView):
    model = Customer
    template_name = "customers/list.html"
    context_object_name = "customers"


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "customers/detail.html"
    context_object_name = "customer"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(user=self.request.user)
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj


class CustomerCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:  # type: ignore
        model = Customer
        fields = ["pan", "name", "ph_no"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        return cleaned_data


class CustomerCreateView(AdminRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerCreationForm
    template_name = "customers/create.html"
    success_url = reverse_lazy("customers-list")

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("Form Invalid")
            # return self.form_invalid(form)
            return render(request, self.template_name, {"form": form})

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


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ["name", "ph_no"]
    template_name = "customers/update.html"
    context_object_name = "customer"
    success_url = reverse_lazy("customer-details")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(user=self.request.user)
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
