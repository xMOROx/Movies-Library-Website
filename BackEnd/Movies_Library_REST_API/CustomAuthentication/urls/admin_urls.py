from CustomAuthentication.views import admin_views
from django.urls import re_path

urlpatterns = [
    re_path(r"^admin/users$", admin_views.UserListView.as_view(), name="admin users"),
    re_path(r"^admin/users/(?P<id>[0-9]+)$", admin_views.UpdateUserView.as_view(), name="admin update user"),
    re_path(r"^admin/users/(?P<id>[0-9]+)/change-password$", admin_views.ChangePasswordForUserView.as_view(),
            name="admin change password"),
    re_path(
        r"^admin/users/(?P<user_id>[0-9]+)/ban$",
        admin_views.BanUserView.as_view(),
        name="admin ban user",
    ),
]
