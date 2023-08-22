from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('cards/', CardListView.as_view(), name='cards-list'),
    path('cards/up/<int:id>', CardUpdateView.as_view(), name='cards-update'),
    path('cards/del/<int:pk>', CardDeleteView.as_view(), name='cards-delete'),
    path('', BalanceListView.as_view(), name='balance-list'),
    # path('<int:id>/', BalanceUpdateView.as_view(), name='balance-update'),
    # path('<int:pk>/del/', BalanceDeleteView.as_view(), name='balance-delete'),
    path('incomes/', IncomeListView.as_view(), name='income-list'),
    path('incomes/<int:pk>', IncomeDetailView.as_view(), name='income-detail'),

    # URL patterns for Expenses objects
    path('expenses/', ExpensesListView.as_view(), name='expenses-list'),
    path('expenses/<int:pk>', ExpensesDetailView.as_view(), name='expenses-detail'),

    ]