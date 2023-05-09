from django.urls import re_path
from ..views import movies_views

urlpatterns = [
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
