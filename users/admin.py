from django.contrib import admin
from .models import UserAccount
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_editable = ('is_active', 'is_staff', 'is_superuser')


admin.site.register(UserAccount, CustomUserAdmin)

