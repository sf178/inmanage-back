from django.contrib import admin
from .models import TemporaryCustomUser, CustomUser, Jwt, Favorite

class TemporaryCustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register((CustomUser, Jwt, Favorite))

admin.site.register(TemporaryCustomUser, TemporaryCustomUserAdmin)
