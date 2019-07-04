from django.contrib import admin
from .models import Region, MVC

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'oktmo_code',  'parent_region', 'status')
    search_fields = ['name']

admin.site.register(Region, RegionAdmin)


class MVCAdmin(admin.ModelAdmin):
    pass

admin.site.register(MVC)