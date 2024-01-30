from django.contrib import admin
from . import models


# Register your models here.
class BalanceAdmin(admin.ModelAdmin):
    pass

class CurrencyAdmin(admin.ModelAdmin):
    pass

class CardAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Balance, BalanceAdmin)
admin.site.register(models.Card, CardAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
