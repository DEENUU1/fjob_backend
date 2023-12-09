from django.contrib import admin
from .models import WorkType, EmploymentType, Experience, Salary, JobOffer


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('salary_from', 'salary_to', 'currency', 'schedule')
    list_filter = ('currency', 'schedule')
    search_fields = ('salary_from', 'salary_to', 'currency', 'schedule')


class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'created_at', 'status')
    list_filter = ('status', 'is_remote', 'is_hybrid', 'work_type', 'employment_type', 'experience')
    search_fields = ('title', 'description', 'company__name', 'skills', 'company_name')
    filter_horizontal = ('addresses', 'salary', 'experience', 'work_type', 'employment_type')
    list_editable = ('status',)


admin.site.register(WorkType)
admin.site.register(EmploymentType)
admin.site.register(Experience)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(JobOffer, JobOfferAdmin)
