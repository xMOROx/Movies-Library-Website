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
        r"^users/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)$",
        user_movies_views.AddMovieToUserView.as_view(),
        name="add movie to user",
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
        name="movie details api",
    ),
    re_path(r"^movies/popular$", movies_views.popular_movies, name="popular movies"),
    re_path(r"^movies/upcoming$", movies_views.upcoming_movies, name="upcoming movies"),
    re_path(r"^movies/latest$", movies_views.latest_movies, name="latest movies"),
    re_path(r"^movies/trending", movies_views.trending_movies, name="trending movies"),
    re_path(
        r"^movies/now_playing", movies_views.now_playing_movies, name="now playing"
    ),
    re_path(
        r"^movies/(?P<movie_id>[0-9]+)/credits$",
        movies_views.movie_credits,
        name="movie credits",
    ),
    re_path(
        r"^movies/(?P<movie_id>[0-9]+)/recommendations$",
        movies_views.movie_recommendations,
        name="recommendations after movie",
    ),
    re_path(
        r"^movies/(?P<movie_id>[0-9]+)/similar$",
        movies_views.similar_movies,
        name="similar movies",
    ),
    re_path(
        r"^movies/(?P<movie_id>[0-9]+)/providers$",
        movies_views.movie_provider,
        name="movie providers",
    ),
]
