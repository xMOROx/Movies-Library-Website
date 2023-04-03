from django.urls import include, re_path, path
from Movies_Library_API import views
from django.contrib import admin
from . import apis

urlpatterns = [
    re_path(r"^movies/users$", views.movie_list, name="movie_list_users"),
    re_path(
        r"^movies/users(?P<pk>[0-9]+)$", views.movie_detail, name="movie_detail_users"
    ),
    re_path(
        r"^movies/(?P<pk>[0-9]+)$", views.movie_details_api, name="movie_details_api"
    ),
    re_path(r"^popular_movies$", views.popular_movies, name="popular_movies"),
    re_path(r"^upcoming_movies$", views.upcoming_movies, name="upcoming_movies"),
    re_path(r"^latest_movies$", views.latest_movies, name="latest_movies"),
    # User endpoints
    re_path(r"^register$", apis.RegisterAPI.as_view(), name="register"),
    re_path(r"^login$", apis.LoginAPI.as_view(), name="login"),
    re_path(r"^logout$", apis.LogoutAPI.as_view(), name="logout"),
    re_path(r"^me$", apis.UserAPI.as_view(), name="me"),
]
