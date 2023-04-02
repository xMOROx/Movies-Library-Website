from django.urls import include, re_path, path
from Movies_Library_API import views


urlpatterns = [
    re_path(r"^api/v1/movies$", views.movie_list),
    re_path(r"^api/v1/movies/(?P<pk>[0-9]+)$", views.movie_detail),
]
