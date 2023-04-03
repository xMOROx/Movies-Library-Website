from django.contrib import admin
from . import models


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    list_display_links = ("id", "username")
    search_fields = ("username",)
    list_filter = ("is_staff", "is_active")
    list_per_page = 25


admin.site.register(models.User, UserAdmin)
