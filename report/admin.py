from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ["user", "offer", "reviewed", "created_at"]
    list_filter = ["reviewed"]
    list_editable = ["reviewed"]
    search_fields = ["user", "offer"]


admin.site.register(Report, ReportAdmin)
