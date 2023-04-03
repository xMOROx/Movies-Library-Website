from django.urls import include, re_path, path
from Movies_Library_API import views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^api-auth/", include("rest_framework.urls")),
    re_path(r"^api/v1/movies$", views.movie_list),
    re_path(r"^api/v1/movies/(?P<pk>[0-9]+)$", views.movie_detail),
    re_path(r"^api/v1/movies_api/(?P<pk>[0-9]+)$", views.movie_details_api),
    re_path(r"^api/v1/popular_movies$", views.popular_movies),
]
