from . import views
from django.urls import re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    re_path(r"^register-user$", views.UserRegisterView.as_view(), name="register"),
    re_path(r"^signin$", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # re_path(r"^signout$", views.UserLogoutView.as_view(), name="logout"),
    re_path(r"^users/(?P<user_id>[0-9]+)$", views.UserView.as_view(), name="user"),
    re_path(r"^token/refresh$", TokenRefreshView.as_view(), name="token_refresh"),
]
