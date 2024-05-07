# authentication/admin.py

from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin



# class CustomUserAdmin(UserAdmin):
#     # Add 'is_evaluator' to the fields displayed in the list view
#     list_display = ('id', 'email', 'fullname', 'is_evaluator')

#     # Customize fieldsets to avoid duplicates and include 'is_evaluator'
#     fieldsets = UserAdmin.fieldsets  # Start with the default UserAdmin fieldsets
#     fieldsets = list(fieldsets)  # Convert to a list to modify it

#     # Add 'is_evaluator' to the first fieldset (basic user information)
#     fieldsets[0] = (None, {'fields': ('email', 'fullname', 'is_evaluator', 'password')})

#     # Recast back to tuple to ensure correct data type
#     fieldsets = tuple(fieldsets)

#     # Allow filtering by 'is_evaluator' in the admin interface
#     list_filter = UserAdmin.list_filter + ('is_evaluator',)

#     # Update search fields to use 'email' and 'fullname'
#     search_fields = ('email', 'fullname')

#     # Change ordering to be by 'email'
#     ordering = ('email',)  # You can also use 'id' or 'fullname'

# # Register the custom admin with the updated fieldsets
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