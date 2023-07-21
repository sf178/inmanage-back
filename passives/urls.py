from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('properties/', PropertyListView.as_view(), name='property-list-create'),
    path('properties/del/<int:pk>', PropertyDeleteView.as_view(), name='property-list-delete'),
    path('properties/up/<int:id>', PropertyUpdateView.as_view(), name='property-list-update'),
    path('property-asset/<int:property_id>', PropertyAssetListView.as_view(), name='property-asset-list'),
    path('property-asset/', PropertyAssetCreateView.as_view(), name='property-asset-create'),
    path('property-asset/del/<int:pk>', PropertyAssetDeleteView.as_view(), name='property-asset-delete'),
    path('property-asset/up/<int:id>', PropertyAssetUpdateView.as_view(), name='property-asset-update'),
    path('transport/', TransportListView.as_view(), name='transport-list-create'),
    path('transport/del/<int:pk>', TransportDeleteView.as_view(), name='transport-list-delete'),
    path('transport/up/<int:id>', TransportUpdateView.as_view(), name='transport-list-update'),
    path('loans/', LoansListView.as_view(), name='loans-list-create'),
    path('loans/del/<int:pk>', LoansDeleteView.as_view(), name='loans-list-delete'),
    path('loans/up/<int:id>', LoansUpdateView.as_view(), name='loans-list-update'),
]

urlpatterns = format_suffix_patterns(urlpatterns)