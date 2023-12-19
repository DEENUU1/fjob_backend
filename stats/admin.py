from django.contrib import admin

from .models import Statistics


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ["model_type", "created_at"]
    search_fields = ["model_type"]
    list_filter = ["model_type"]


admin.site.register(Statistics, StatisticsAdmin)
