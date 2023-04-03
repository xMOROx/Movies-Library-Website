from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_staff", "is_superuser", "is_active")
    list_display_links = ["id", "email"]
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser")
    list_per_page = 25


admin.site.register(models.User, UserAdmin)
