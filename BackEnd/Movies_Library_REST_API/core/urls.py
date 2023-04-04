from django.contrib import admin
from django.urls import include, re_path, path


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^api/v1/", include("Movies_Library_API.urls")),
    re_path(r"^auth/", include("Authentication.urls")),
]
