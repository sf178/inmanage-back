from django.contrib import admin

# Register your models here.
from . import models
from .models import PropertyAsset, BusinessAsset
#from .models import *


class ProfileAdmin(admin.ModelAdmin):
    pass


# class CardAdmin(admin.ModelAdmin):
#     pass


class ActivesAdmin(admin.ModelAdmin):
    pass


class PropertyAssetInline(admin.TabularInline):
    model = PropertyAsset
    extra = 0


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyAssetInline]
    list_display = (
    'id', 'user_id', 'name', 'address', 'owner', 'rent_type', 'bought_price', 'actual_price', 'initial_payment',
    'loan_term', 'percentage', 'month_payment', 'revenue', 'equipment_price', 'month_income', 'month_expense',
    'average_profit'
    )
    list_filter = ('user_id', 'name', 'owner', 'rent_type')
    search_fields = ('name', 'address', 'owner')


class PropertyAssetAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'name', 'property_id', 'price'
    )
    list_filter = ('name', 'property_id')
    search_fields = ('name', 'property_id')


class TransportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'name', 'owner', 'owner_type', 'vin', 'use', 'bought_price', 'initial_payment', 'loan_term',
        'percentage', 'month_payment', 'month_income', 'month_expense', 'average_profit', 'revenue'
    )
    list_filter = ('user_id', 'name', 'owner', 'owner_type', 'use')
    search_fields = ('name', 'owner', 'vin')


class BusinessAssetInline(admin.TabularInline):
    model = BusinessAsset
    extra = 0


class BusinessAdmin(admin.ModelAdmin):
    inlines = [BusinessAssetInline]
    list_display = (
        'id', 'name', 'address', 'user_id', 'type', 'direction',
        'month_income', 'month_expense', 'average_profit', 'revenue'
    )
    list_filter = ('user_id', 'type', 'direction')
    search_fields = ('name', 'address')


class BusinessAssetAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'business_id', 'price'
    )
    list_filter = ('name', 'business_id')
    search_fields = ('name', 'business_id')


class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'SHORTNAME', 'OPEN', 'LOW', 'HIGH')
    list_filter = ('SHORTNAME',)
    search_fields = ('SHORTNAME',)
    ordering = ['id']


class BondsAdmin(admin.ModelAdmin):
    list_display = ('id', 'SHORTNAME', 'OPEN', 'LOW', 'HIGH', 'MARKETPRICE2', 'MARKETPRICE3')
    list_filter = ('SHORTNAME',)
    search_fields = ('SHORTNAME',)
    ordering = ['id']
    pass


admin.site.register(models.ObjectsProfile, ProfileAdmin)
#admin.site.register(models.Card, CardAdmin)
admin.site.register(models.Actives, ActivesAdmin)
admin.site.register(models.Property, PropertyAdmin)
admin.site.register(models.PropertyAsset, PropertyAssetAdmin)
admin.site.register(models.Transport, TransportAdmin)
admin.site.register(models.Business, BusinessAdmin)
admin.site.register(models.BusinessAsset, BusinessAssetAdmin)
admin.site.register(models.Stocks, StockAdmin)
admin.site.register(models.Bonds, BondsAdmin)
