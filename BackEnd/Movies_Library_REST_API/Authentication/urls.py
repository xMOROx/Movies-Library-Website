from . import views
from django.urls import re_path


urlpatterns = [
    # User endpoints
    re_path(r"^register$", views.RegisterAPI.as_view(), name="register"),
    re_path(r"^login$", views.LoginAPI.as_view(), name="login"),
    re_path(r"^logout$", views.LogoutAPI.as_view(), name="logout"),
    re_path(r"^me$", views.UserAPI.as_view(), name="me"),
]
