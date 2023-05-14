from django.urls import re_path
from ..views import user_movies_views

urlpatterns = [
    re_path(
        r"^users/(?P<user_id>[0-9]+)/movies$",
        user_movies_views.list_of_details_for_movies_per_user,
        name="details of user movies",
    ),
    re_path(
        r"^users/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)/details$",
        user_movies_views.details_of_movie_for_user,
        name="details of movie for user",
    ),
    re_path(
        r"^users/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)$",
        user_movies_views.add_movie_to_user,
        name="add movie to user",
    ),
]
