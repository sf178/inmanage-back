from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('properties/', PropertyListView.as_view(), name='property-list-create'),
    path('properties/del/<int:pk>/', PropertyDeleteView.as_view(), name='property-list-delete'),
    path('properties/up/<int:id>', PropertyUpdateView.as_view(), name='property-list-update'),
    path('transport/', TransportListView.as_view(), name='transport-list-create'),
    path('transport/del/<int:pk>/', TransportDeleteView.as_view(), name='transport-list-delete'),
    path('transport/up/<int:id>', TransportUpdateView.as_view(), name='transport-list-update'),
    path('loans/', LoansListView.as_view(), name='loans-list-create'),
    path('loans/del/<int:pk>/', LoansDeleteView.as_view(), name='loans-list-delete'),
    path('loans/up/<int:id>', LoansUpdateView.as_view(), name='loans-list-update'),
    path('borrows/', BorrowListView.as_view(), name='borrows-list-create'),
    path('borrows/del/<int:pk>/', BorrowDeleteView.as_view(), name='borrows-list-delete'),
    path('borrows/up/<int:id>', BorrowUpdateView.as_view(), name='borrows-list-update'),
    path('', PassivesListView.as_view(), name='passives-list'),
    # URL patterns for Expenses objects
    path('expenses/', ExpensesListView.as_view(), name='expenses-list'),
    path('expenses/<int:pk>', ExpensesDetailView.as_view(), name='expenses-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)