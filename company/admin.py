from django.contrib import admin

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_size', 'description', 'user', 'created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'company_size', 'description', 'user')
    list_editable = ('is_active', )


admin.site.register(Company, CompanyAdmin)
