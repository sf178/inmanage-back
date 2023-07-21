from django.contrib import admin
from .models import Car


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('mark', 'model', 'price', 'year', 'km_age')
    search_fields = ('mark', 'model', 'year')