from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "default_currency", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
