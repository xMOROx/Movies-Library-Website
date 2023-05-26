from CustomAuthentication import admin_views
from CustomAuthentication import views
from django.urls import re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    re_path(r"^register-user$", views.UserRegisterView.as_view(), name="register"),
    re_path(r"^signin$", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"^users/(?P<user_id>[0-9]+)$", views.UserView.as_view(), name="users"),
    re_path(r"^users/(?P<user_id>[0-9]+)/change-password$", views.ChangePasswordView.as_view(), name="change password"),
    re_path(r"^token/refresh$", TokenRefreshView.as_view(), name="token_refresh"),

    re_path(r"^admin/users$", admin_views.UserListView.as_view(), name="admin users"),
    re_path(r"^admin/users/(?P<id>[0-9]+)$", admin_views.UpdateUserView.as_view(), name="admin update user"),
    re_path(r"^admin/users/(?P<id>[0-9]+)/change-password$", admin_views.ChangePasswordForUserView.as_view(),
            name="admin change password"),
]
