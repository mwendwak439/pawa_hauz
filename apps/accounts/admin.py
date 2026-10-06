from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Extends Django's built-in UserAdmin so we keep all the standard
    password, permission, and group controls, plus our custom fields.
    """

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Gym Profile', {'fields': ('role', 'phone_number')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Gym Profile', {'fields': ('role', 'phone_number')}),
    )