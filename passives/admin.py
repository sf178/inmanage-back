from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Loans, Property, Transport

admin.site.register(Loans)
admin.site.register(Property)
admin.site.register(Transport)