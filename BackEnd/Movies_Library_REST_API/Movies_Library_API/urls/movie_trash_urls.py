from django.urls import re_path
from ..views import movie_trash_views

urlpatterns = [
    re_path(
        r"^trash/users/(?P<user_id>[0-9]+)/movies$",
        movie_trash_views.get_all_movies,
        name="get all movies from trash for user",
    ),
    re_path(
        r"^trash/users/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)$",
        movie_trash_views.crud_for_movie_inside_trash,
        name="get movie from trash",
    )

]