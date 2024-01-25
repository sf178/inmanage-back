from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    #path('properties/get', PropertyListGetView.as_view(), name='property-list-get'),
    #path('properties/delete/<int:pk>', PropertyDeleteView.as_view(), name='property-list-delete'),
    #path('properties/update/<int:pk>', PropertyUpdateView.as_view(), name='property-list-update'),

    path('properties/', PropertyListView.as_view(), name='property-list-create'),
    path('properties/del/<int:pk>/', PropertyDeleteView.as_view(), name='property-list-delete'),
    path('properties/up/<int:id>', PropertyUpdateView.as_view(), name='property-list-update'),
    path('transport/', TransportListView.as_view(), name='transport-list-create'),
    path('transport/del/<int:pk>/', TransportDeleteView.as_view(), name='transport-list-delete'),
    path('transport/up/<int:id>', TransportUpdateView.as_view(), name='transport-list-update'),
    path('business/', BusinessListView.as_view(), name='business-list-create'),
    path('business/del/<int:pk>/', BusinessDeleteView.as_view(), name='business-list-delete'),
    path('business/up/<int:id>', BusinessUpdateView.as_view(), name='business-list-update'),

    path('jewelry/', JewelryListView.as_view(), name='jewelry-list'),
    # path('jewelry/create/', JewelryCreateView.as_view(), name='jewelry-create'),
    path('jewelry/<int:pk>/', JewelryDetailView.as_view(), name='jewelry-detail'),
    path('jewelry/up/<int:pk>/', JewelryUpdateView.as_view(), name='jewelry-update'),
    path('jewelry/del/<int:pk>/', JewelryDeleteView.as_view(), name='jewelry-delete'),

    # Securities URLs
    path('securities/', SecuritiesListView.as_view(), name='securities-list'),
    # path('securities/create/', SecuritiesCreateView.as_view(), name='securities-create'),
    path('securities/<int:pk>/', SecuritiesDetailView.as_view(), name='securities-detail'),
    path('securities/up/<int:pk>/', SecuritiesUpdateView.as_view(), name='securities-update'),
    path('securities/del/<int:pk>/', SecuritiesDeleteView.as_view(), name='securities-delete'),

    path('incomes/', IncomeListView.as_view(), name='income-list'),
    path('incomes/<int:pk>', IncomeDetailView.as_view(), name='income-detail'),
    # URL patterns for Expenses objects
    path('expenses/', ExpensesListView.as_view(), name='expenses-list'),
    path('expenses/<int:pk>', ExpensesDetailView.as_view(), name='expenses-detail'),
    path('', ActiveList.as_view(), name='active-list'),


]

urlpatterns = format_suffix_patterns(urlpatterns)
