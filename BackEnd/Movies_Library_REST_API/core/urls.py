from django.contrib import admin
from django.urls import include, re_path, path


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^api/v1/", include("Movies_Library_API.urls.movies_urls")),
    re_path(r"^api/v1/", include("Movies_Library_API.urls.tv_shows_urls")),
    re_path(r"^api/v1/", include("Movies_Library_API.urls.actors_urls")),
    re_path(r"^api/v1/", include("Movies_Library_API.urls.users_urls")),
    re_path(r"^api/v1/", include("Movies_Library_API.urls.movie_trash_urls")),
    re_path(r"^api/v1/", include("Movies_Library_API.urls.tv_show_trash_urls")),
    re_path(r"^api/v1/auth/", include("CustomAuthentication.urls.auth_urls")),
    re_path(r"^api/v1/admin", include("CustomAuthentication.urls.admin_urls")),
]
