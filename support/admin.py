from django.contrib import admin

from .models import Contact, Report


class ContactAdmin(admin.ModelAdmin):
    list_display = ["subject", "email", "reviewed", "created_at"]
    list_filter = ["reviewed", "created_at"]
    search_fields = ["subject", "email"]
    list_editable = ["reviewed"]


class ReportAdmin(admin.ModelAdmin):
    list_display = ["user", "offer", "reviewed", "created_at"]
    list_filter = ["reviewed", "created_at"]
    search_fields = ["user", "offer"]
    list_editable = ["reviewed"]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Report, ReportAdmin)
