from . import views
from django.urls import re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    re_path(r"^register-user$", views.UserRegisterView.as_view(), name="register"),
    re_path(r"^signin$", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"^users$(?P<user_id>[0-9]+)$", views.UserView.as_view(), name="users"),
    re_path(r"^admin/users$", views.UserListView.as_view(), name="admin users"),
    re_path(
        r"^admin/users/(?P<user_id>[0-9]+)$",
        views.AdminUserUpdateView.as_view(),
        name="admin update user",
    ),
    re_path(
        r"^admin/users/(?P<user_id>[0-9]+)/ban$",
        views.BanUserView.as_view(),
        name="signout",
    ),
    re_path(r"^token/refresh$", TokenRefreshView.as_view(), name="token_refresh"),
]
