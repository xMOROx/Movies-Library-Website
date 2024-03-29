from CustomAuthentication import models
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    """
        Admin class for User model

    """
    list_display = ("id", "email", "is_staff", "is_superuser", "is_active", "is_banned")
    list_display_links = ["id", "email"]
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser")
    list_per_page = 25


admin.site.register(models.User, UserAdmin)
