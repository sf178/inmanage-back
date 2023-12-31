from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    #path('properties/get', PropertyListGetView.as_view(), name='property-list-get'),
    #path('properties/delete/<int:pk>', PropertyDeleteView.as_view(), name='property-list-delete'),
    #path('properties/update/<int:pk>', PropertyUpdateView.as_view(), name='property-list-update'),

    path('properties/', PropertyListView.as_view(), name='property-list-create'),
    path('properties/del/<int:pk>', PropertyDeleteView.as_view(), name='property-list-delete'),
    path('properties/up/<int:id>', PropertyUpdateView.as_view(), name='property-list-update'),
    path('transport/', TransportListView.as_view(), name='transport-list-create'),
    path('transport/del/<int:pk>', TransportDeleteView.as_view(), name='transport-list-delete'),
    path('transport/up/<int:id>', TransportUpdateView.as_view(), name='transport-list-update'),
    path('business/', BusinessListView.as_view(), name='business-list-create'),
    path('business/del/<int:pk>', BusinessDeleteView.as_view(), name='business-list-delete'),
    path('business/up/<int:id>', BusinessUpdateView.as_view(), name='business-list-update'),
    path('property-asset/<int:property_id>', PropertyAssetListView.as_view(), name='property-asset-list'),
    path('property-asset/', PropertyAssetCreateView.as_view(), name='property-asset-create'),
    path('property-asset/del/<int:pk>', PropertyAssetDeleteView.as_view(), name='property-asset-delete'),
    path('property-asset/up/<int:id>', PropertyAssetUpdateView.as_view(), name='property-asset-update'),
    path('business-asset/<int:business_id>', BusinessAssetListView.as_view(), name='business-asset-list'),
    path('business-asset/', BusinessAssetCreateView.as_view(), name='business-asset-create'),
    path('business-asset/del/<int:pk>', BusinessAssetDeleteView.as_view(), name='business-asset-delete'),
    path('business-asset/up/<int:id>', BusinessAssetUpdateView.as_view(), name='business-asset-update'),
    path('actives_scripts/', ActiveList.as_view(), name='active-list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)