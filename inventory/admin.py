from django.contrib import admin
from .models import *


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'launch_status', 'total_actives_cost', 'created_at']
    search_fields = ['user__username', 'launch_status']


@admin.register(InventoryAsset)
class InventoryAssetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'added', 'price', 'flag', 'created_at']
    search_fields = ['user__username', 'added']


# @admin.register(PreviousInventory)
# class PreviousInventoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'launch_status', 'total_actives_cost', 'created_at']
#     search_fields = ['user__username', 'launch_status']