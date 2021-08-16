from django.contrib import admin

from .models import HotelsLocation


@admin.register(HotelsLocation)
class HotelsLocationAdmin(admin.ModelAdmin):
    pass


# Register your models here.

