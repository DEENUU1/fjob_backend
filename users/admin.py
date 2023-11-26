from django.contrib import admin
from .models import UserAccount, Company
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_editable = ('is_active', 'is_staff', 'is_superuser')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_size', 'description', 'user', 'created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'company_size', 'description', 'user')
    list_editable = ('is_active',)


admin.site.register(UserAccount, CustomUserAdmin)
admin.site.register(Company, CompanyAdmin)
