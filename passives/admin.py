from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


class LoansAdmin(admin.ModelAdmin):
    pass


class PropertyAdmin(admin.ModelAdmin):
    pass

class MainPropertyAdmin(admin.ModelAdmin):
    pass

class MainTransportAdmin(admin.ModelAdmin):
    pass

class MainLoansAdmin(admin.ModelAdmin):
    pass

class TransportAdmin(admin.ModelAdmin):
    pass


class PassivesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Loans, LoansAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(Passives, PassivesAdmin)
admin.site.register(MainTransport, MainTransportAdmin)
admin.site.register(MainLoans, MainLoansAdmin)
admin.site.register(MainProperties, MainPropertyAdmin)