from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('cards/', CardListView.as_view(), name='cards-list'),
    path('cards/<int:id>/', CardUpdateView.as_view(), name='cards-update'),
    path('cards/<int:pk>/del/', CardDeleteView.as_view(), name='cards-delete'),
    path('', BalanceListView.as_view(), name='balance-list'),
    path('<int:id>/', BalanceUpdateView.as_view(), name='balance-update'),
    path('<int:pk>/del/', BalanceDeleteView.as_view(), name='balance-delete')
    ]