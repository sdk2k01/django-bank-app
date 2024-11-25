from django.contrib.auth.views import LoginView, LogoutView
from django.urls.base import reverse_lazy


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self) -> str:
        redirect_to = self.request.GET.get("next")
        # TBD: Ensure URL is safe
        if redirect_to:
            return redirect_to

        if self.request.user.is_staff or self.request.user.is_superuser:
            return reverse_lazy("customers-list")  # URL name for "customers/"
        else:
            return reverse_lazy("customer-details")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")
