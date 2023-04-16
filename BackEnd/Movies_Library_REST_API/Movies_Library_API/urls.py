from django.urls import re_path
from .views import movies_views, user_movies_views
from .views import admin_views as auth_views

urlpatterns = [
    re_path(
        r"^users/(?P<user_id>[0-9]+)/movies/details$",
        movies_views.list_of_details_for_movies_per_user,
        name="details of user movies",
    ),
    re_path(
        r"^users/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)/details$",
        movies_views.details_of_movie_for_user,
        name="details of movie for user",
    ),
    re_path(
        r"^admin/users$", auth_views.AdminUserListView.as_view(), name="admin users"
    ),
    re_path(
        r"^admin/users/(?P<user_id>[0-9]+)$",
        auth_views.AdminUserUpdateView.as_view(),
        name="admin update user",
    ),
    re_path(
        r"^admin/users/(?P<user_id>[0-9]+)/ban$",
        auth_views.BanUserView.as_view(),
        name="admin ban user",
    ),
    re_path(
        r"^movies/(?P<movie_id>[0-9]+)$",
        movies_views.movie_details_api,
        name="movie_details_api",
    ),
    re_path(
        r"^users/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)$",
        user_movies_views.AddMovieToUserView.as_view(),
        name="add movie to user",
    ),
    re_path(r"^popular_movies$", movies_views.popular_movies, name="popular_movies"),
    re_path(r"^upcoming_movies$", movies_views.upcoming_movies, name="upcoming_movies"),
    re_path(r"^latest_movies$", movies_views.latest_movies, name="latest_movies"),
]
