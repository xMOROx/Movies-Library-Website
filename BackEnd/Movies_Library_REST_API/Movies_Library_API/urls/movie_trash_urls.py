from django.urls import re_path
from ..views import movie_trash_views

urlpatterns = [
    re_path(
        r"^trash/user/(?P<user_id>[0-9]+)/movies$",
        movie_trash_views.get_all_movies,
        name="get all movies from trash for user",
    ),
    re_path(
        r"^trash/user/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)$",
        movie_trash_views.get_movie_by_id,
        name="get movie from trash",
    ),
    re_path(
        r"^trash/user/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)/add$",
        movie_trash_views.add_movie_to_trash,
        name="add movie to trash",
    ),
    re_path(
        r"^trash/user/(?P<user_id>[0-9]+)/movies/(?P<movie_id>[0-9]+)/delete$",
        movie_trash_views.delete_movie_from_trash,
        name="delete movie from trash",
    ),

]