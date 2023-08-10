from django.contrib import admin
from .models import Inventory, InventoryAsset


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'launch_status', 'total_cost', 'created_at']
    search_fields = ['user__username', 'launch_status']


@admin.register(InventoryAsset)
class InventoryAssetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'added', 'price', 'flag', 'created_at']
    search_fields = ['user__username', 'added']
