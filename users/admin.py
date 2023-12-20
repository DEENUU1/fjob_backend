from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserAccount


class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'account_type')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_editable = ('is_active', 'is_staff', 'is_superuser', 'account_type')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        kwargs['exclude'] = ('date_joined', 'username')
        return super().get_form(request, obj, **kwargs)


admin.site.register(UserAccount, CustomUserAdmin)
