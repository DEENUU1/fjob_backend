from django.contrib import admin
from .models import Candidate, OfferCandidate


class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone']
    search_fields = ['full_name', 'email', 'phone']
    list_filter = ['full_name', 'email', 'phone']


class OfferCandidateAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'offer', 'status']
    search_fields = ['candidate', 'offer', 'status']
    list_filter = ['candidate', 'offer', 'status']
    list_editable = ['status']


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(OfferCandidate, OfferCandidateAdmin)
