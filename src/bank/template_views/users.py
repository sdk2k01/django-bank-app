from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self) -> str:
        redirect_to = self.request.GET.get(
            "next", f"/customers/{self.request.user.customer_profile.cif}"
        )
        # TBD: Ensure URL is safe
        if redirect_to:
            return redirect_to
