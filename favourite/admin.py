from django.contrib import admin
from .models import Favourite


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'offer']


admin.site.register(Favourite, FavouriteAdmin)
