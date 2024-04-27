# authentication/admin.py

from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# class CustomUserAdmin(UserAdmin):
#     list_display = ('id', 'username', 'email')  # Display only 'id', 'username', and 'email' fields

# admin.site.register(User, CustomUserAdmin)

class CustomUserAdmin(UserAdmin):
    # Add 'is_evaluator' to the fields displayed in the list view
    list_display = ('id', 'username', 'email', 'is_evaluator')

    # Define which fields to display in the user admin form
    fieldsets = (
        (None, {'fields': ('is_evaluator',)}),  # Include 'is_evaluator' in the admin form
    ) + UserAdmin.fieldsets

    # Allow filtering by 'is_evaluator' in the admin interface
    list_filter = UserAdmin.list_filter + ('is_evaluator',)

admin.site.register(User, CustomUserAdmin)