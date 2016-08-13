from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .forms import *
from .models import Client

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'email',
        'is_staff',
        'failed_login_attempts',
        'last_login',
    )

    list_filter = (
        'is_staff',
        'account_locked',
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
            )}
        ),
    )

    search_fields = (
        'email',
        'first_name',
        'last_name',
    )

    ordering = ('email',)

    filter_horizontal = ()

admin.site.register(Client, UserAdmin)
