"""
URL configuration for bankapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from bank import views

# router = DefaultRouter()
# router.register(r'customers', views.CustomerViewSet, basename='customer')

urlpatterns = [
    # path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path("register/", views.RegisterCustomerView.as_view()),
    path("api-auth/", include("rest_framework.urls")),
    # Customer Actions
    path("customers/", views.CustomersView.as_view()),
    path("customers/<int:pk>/", views.CustomerView.as_view()),
    # Account Actions
    path("accounts/", views.ListAccountsView.as_view()),
    path("accounts/details/<str:ac_no>/", views.CustomerAccountsView.as_view()),
    path("accounts/create/", views.AccountCreationView.as_view()),
    # Card Actions
    path("cards/", views.ListCardsView.as_view()),
    path("cards/create/<str:ac_no>/", views.CardsCreationView.as_view()),
    path("cards/details/<str:card_no>/", views.AccountCardsView.as_view()),
    # Banking Actions
    path("deposit/", views.Deposit.as_view()),
    path("withdraw/", views.Withdraw.as_view()),
    path("transactions/", views.ListTransactions.as_view()),
    path("transactions/<int:pk>/", views.UserTransactions.as_view()),
    path("transactions/details/<int:pk>", views.TransactionDetails.as_view()),
]
