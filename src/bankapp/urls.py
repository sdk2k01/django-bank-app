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
from django.urls import include, path

from bank import views
from bank.template_views import (
    CustomLoginView,
    CustomLogoutView,
    accounts,
    actions,
    cards,
    customers,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    # API-v1 #
    # Customer Actions
    path("api/v1/customers/", views.CustomersView.as_view()),
    path("api/v1/customers/<int:pk>/", views.CustomerView.as_view()),
    # Account Actions
    path("api/v1/accounts/", views.ListAccountsView.as_view()),
    path("api/v1/accounts/details/<str:ac_no>/", views.CustomerAccountsView.as_view()),
    path("api/v1/accounts/create/", views.AccountCreationView.as_view()),
    # Card Actions
    path("api/v1/cards/", views.ListCardsView.as_view()),
    path("api/v1/cards/create/<str:ac_no>/", views.CardsCreationView.as_view()),
    path("api/v1/cards/details/<str:card_no>/", views.AccountCardsView.as_view()),
    # Banking Actions
    path("api/v1/deposit/", views.Deposit.as_view()),
    path("api/v1/withdraw/", views.Withdraw.as_view()),
    path("api/v1/transactions/", views.ListTransactions.as_view()),
    path("api/v1/transactions/user/", views.UserTransactions.as_view()),
    path("api/v1/transactions/details/<int:pk>", views.TransactionDetails.as_view()),
    # UI #
    # Login/Logout User
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    # Customer URLs
    path(
        "customers/",
        customers.CustomerListView.as_view(),
        name="customers-list",
    ),
    path(
        "customers/create/",
        customers.CustomerCreateView.as_view(),
        name="customer-create-template",
    ),
    path(
        "customer/profile/",
        customers.CustomerDetailView.as_view(),
        name="customer-details",
    ),
    path(
        "customer/profile/edit/",
        customers.CustomerUpdateView.as_view(),
        name="edit-customer-details",
    ),
    # Account URLs
    # Savings Account
    path(
        "accounts/sb/",
        accounts.SavingsAccountListView.as_view(),
        name="savings-accounts-list",
    ),
    path(
        "accounts/sb/create/",
        accounts.SavingsAccountCreationView.as_view(),
        name="savings-account-creation-template",
    ),
    path(
        "accounts/sb/<str:pk>/",
        accounts.SavingsAccountDetailView.as_view(),
        name="savings-account-details",
    ),
    # Current Account
    path(
        "accounts/ca/",
        accounts.CurrentAccountListView.as_view(),
        name="current-accounts-list",
    ),
    path(
        "accounts/ca/create/",
        accounts.CurrentAccountCreationView.as_view(),
        name="current-account-creation-template",
    ),
    path(
        "accounts/ca/<str:pk>/",
        accounts.CurrentAccountDetailView.as_view(),
        name="current-account-details",
    ),
    # Cards
    # Credit Card
    path(
        "cards/cc/",
        cards.CreditCardListView.as_view(),
        name="credit-cards-list",
    ),
    path(
        "cards/cc/create/",
        cards.CreditCardCreationView.as_view(),
        name="credit-card-creation-template",
    ),
    path(
        "cards/cc/<str:pk>/",
        cards.CreditCardDetailView.as_view(),
        name="credit-card-detials",
    ),
    # Debit Card
    path(
        "cards/dc/",
        cards.DebitCardListView.as_view(),
        name="debit-cards-list",
    ),
    path(
        "cards/dc/create/",
        cards.DebitCardCreationView.as_view(),
        name="debit-card-creation-template",
    ),
    path(
        "cards/dc/<str:pk>/",
        cards.DebitCardDetailView.as_view(),
        name="debit-card-details",
    ),
    # Actions
    # Deposit
    path(
        "deposit/",
        actions.DepositCreationView.as_view(),
        name="deposit-creation-template",
    ),
    # Withdraw
    path(
        "withdraw/",
        actions.WithdrawCreationView.as_view(),
        name="withdraw-creation-template",
    ),
    # Transactions
    path(
        "transactions/",
        actions.TransactionsListView.as_view(),
        name="transactions-list",
    ),
    path(
        "transactions/<int:pk>/",
        actions.TransactionDetailView.as_view(),
        name="transaction-details",
    ),
]
