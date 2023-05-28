from Movies_Library_API.views import admin_views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(
        r"^admin/users$", auth_views.AdminUserListView.as_view(), name="admin users"
    ),
    re_path(
        r"^admin/users/(?P<user_id>[0-9]+)$",
        auth_views.AdminUserUpdateView.as_view(),
        name="admin update user",
    ),
    re_path(
        r"^admin/users/(?P<user_id>[0-9]+)/ban$",
        auth_views.BanUserView.as_view(),
        name="admin ban user",
    ),
]
