from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email', 'reviewed', 'created_at',]
    search_fields = ['subject', 'email', 'message']
    list_editable = ['reviewed']


admin.site.register(Contact, ContactAdmin)