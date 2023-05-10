from django.urls import re_path
from ..views import movies_views, user_movies_views

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
]
