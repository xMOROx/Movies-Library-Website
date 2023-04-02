from django.contrib import admin
from django.urls import include, re_path


urlpatterns = [
    re_path(r"^", include("Movies_Library_API.urls")),
]
