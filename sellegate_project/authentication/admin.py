# authentication/admin.py

from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email')  # Display only 'id', 'username', and 'email' fields

admin.site.register(User, CustomUserAdmin)