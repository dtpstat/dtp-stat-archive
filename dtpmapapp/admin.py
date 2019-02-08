from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MVC)
class MVCAdmin(admin.ModelAdmin):
    pass