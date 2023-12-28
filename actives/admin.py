from django.contrib import admin

# Register your models here.
from . import models
#from .models import PropertyAsset, BusinessAsset
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    pass


# class CardAdmin(admin.ModelAdmin):
#     pass


class ActivesAdmin(admin.ModelAdmin):
    pass

class MainPropertyAdmin(admin.ModelAdmin):
    pass

class MainTransportAdmin(admin.ModelAdmin):
    pass

class MainBusinessAdmin(admin.ModelAdmin):
    pass


class PropertyAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user_id', 'name', 'city', 'street', 'square', 'owner', 'rent_type', 'bought_price', 'actual_price', 'initial_payment',
    'loan_term', 'percentage', 'month_payment', 'revenue', 'equipment_price', 'month_income', 'month_expense',
    'average_profit'
    )
    list_filter = ('user_id', 'name', 'owner', 'rent_type')
    search_fields = ('name', 'city', 'street', 'square', 'owner')


class TransportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'mark', 'model', 'owner', 'owner_type', 'vin', 'use', 'bought_price', 'initial_payment', 'loan_term',
        'percentage', 'month_payment', 'month_income', 'month_expense', 'average_profit', 'revenue'
    )
    list_filter = ('user_id', 'mark', 'model', 'owner', 'owner_type', 'use')
    search_fields = ('mark', 'model', 'owner', 'vin')


class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'address', 'user_id', 'type', 'direction',
        'month_income', 'month_expense', 'average_profit', 'revenue'
    )
    list_filter = ('user_id', 'type', 'direction')
    search_fields = ('name', 'address')


admin.site.register(Actives, ActivesAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(MainTransport, MainTransportAdmin)
admin.site.register(MainBusinesses, MainBusinessAdmin)
admin.site.register(MainProperties, MainPropertyAdmin)

