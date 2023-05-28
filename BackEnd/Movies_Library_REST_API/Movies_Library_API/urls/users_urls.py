from Movies_Library_API.views import user_movies_views, user_tv_show_views
from django.urls import re_path

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
    re_path(
        r"^users/(?P<user_id>[0-9]+)/recommendations$",
        user_movies_views.recommendations,
        name="recommendations",
    ),
    re_path(
        r"^users/(?P<user_id>[0-9]+)/tv$",
        user_tv_show_views.list_of_details_for_tv_show_per_user,
        name="details of user tv shows",
    ),
    re_path(
        r"^users/(?P<user_id>[0-9]+)/tv/(?P<tv_show_id>[0-9]+)/details$",
        user_tv_show_views.details_of_tv_show_for_user,
        name="details of tv show for user",
    ),
    re_path(
        r"^users/(?P<user_id>[0-9]+)/tv/(?P<tv_show_id>[0-9]+)$",
        user_tv_show_views.add_tv_show_to_user,
        name="add movie to user",
    ),
    # re_path(r"^users/(?P<user_id>[0-9]+)/recommendations$", user_movies_views.recommendations, name="recommendations"),
]
