from django.contrib import admin
from .models import Candidate


class CandidateAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "created_at", "status"]
    list_filter = ["status"]
    search_fields = ["first_name", "last_name", "email"]


admin.site.register(Candidate, CandidateAdmin)

