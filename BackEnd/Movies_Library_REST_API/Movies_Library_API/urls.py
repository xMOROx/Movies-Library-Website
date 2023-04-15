from django.urls import re_path
from Movies_Library_API import views

urlpatterns = [
    re_path(
        r"^users/(?P<user_id>[0-9]+)/movies$",
        views.movie_list,
        name="movie_list_users",
    ),
    re_path(
        r"^users/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)$",
        views.movie_detail,
        name="movie_detail_users",
    ),
    re_path(
        r"^movies/(?P<movie_id>[0-9]+)$",
        views.movie_details_api,
        name="movie_details_api",
    ),
    re_path(r"^popular_movies$", views.popular_movies, name="popular_movies"),
    re_path(r"^upcoming_movies$", views.upcoming_movies, name="upcoming_movies"),
    re_path(r"^latest_movies$", views.latest_movies, name="latest_movies"),
]
