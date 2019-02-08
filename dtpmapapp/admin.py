from django.contrib import admin
from . import models


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MVC)
class MVCAdmin(admin.ModelAdmin):
    pass