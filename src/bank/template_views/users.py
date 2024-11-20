from django.contrib.auth.views import LoginView, LogoutView
from django.urls.base import reverse_lazy


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self) -> str:
        redirect_to = self.request.GET.get("next", f"/customer/profile/")
        # TBD: Ensure URL is safe
        if redirect_to:
            return redirect_to


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")
