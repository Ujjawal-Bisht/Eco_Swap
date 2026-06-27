# pyrefly: ignore [missing-import]
from django.contrib import admin
# pyrefly: ignore [missing-import]
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Registers our custom User with Django's built-in UserAdmin instead of the
    plain admin.ModelAdmin. UserAdmin renders the password field with a
    'change password' link and hashes the password via clean_password()
    instead of saving it in plain text whenever a user is created/edited
    through the admin.
    """
    fieldsets = UserAdmin.fieldsets + (
        ('EcoSwap Profile', {'fields': ('role', 'location', 'sustainability_interests', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('EcoSwap Profile', {'fields': ('role', 'location', 'sustainability_interests', 'profile_image')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
