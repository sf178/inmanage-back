from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', InventoryListView.as_view(), name='inv-list-get'),
    path('up/<int:id>', InventoryUpdateView.as_view(), name='inv-list-update'),
    path('asset/up/<int:id>', InventoryAssetUpdateView.as_view(), name='inv-asset-list-update'),
    path('asset/del/<int:id>', InventoryAssetDeleteView.as_view(), name='inv-asset-del-update'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
