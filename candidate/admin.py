from django.contrib import admin

from .models import Candidate


class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'status']
    search_fields = ['email', 'phone']
    list_filter = ['email', 'phone']
    list_editable = ['status']


admin.site.register(Candidate, CandidateAdmin)
