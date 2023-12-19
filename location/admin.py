from django.contrib import admin

from .models import Country, Region, City, Address


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'country')
    list_filter = ('region',)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'country')
    list_filter = ('country',)


admin.site.register(Address, AddressAdmin)
admin.site.register(Country)
admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)
