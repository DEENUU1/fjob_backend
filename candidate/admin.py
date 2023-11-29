from django.contrib import admin
from .models import Candidate


class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone']
    search_fields = ['full_name', 'email', 'phone']
    list_filter = ['full_name', 'email', 'phone']


admin.site.register(Candidate, CandidateAdmin)
