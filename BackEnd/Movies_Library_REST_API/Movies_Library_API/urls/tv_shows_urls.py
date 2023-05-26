from django.urls import re_path
from ..views import tv_shows_views

urlpatterns = [
    re_path(
        r"^tv/(?P<tv_show_id>[0-9]+)$",
        tv_shows_views.tv_show_details_api,
        name="tv show details api",
    ),
    re_path(r"^tv/popular$", tv_shows_views.popular_tv_shows, name="popular tv shows"),
    re_path(r"^yv/upcoming$", tv_shows_views.upcoming_tv_shows, name="upcoming tv shows"),
    re_path(r"^tv/latest$", tv_shows_views.latest_tv_shows, name="latest tv shows"),
    re_path(r"^tv/trending", tv_shows_views.trending_tv_shows, name="trending tv shows"),
    re_path(
        r"^tv/airing_today", tv_shows_views.airing_today, name="airing today"
    ),
    re_path(
        r"^tv/(?P<tv_show_id>[0-9]+)/credits$",
        tv_shows_views.tv_show_credits,
        name="tv show credits",
    ),
    re_path(
        r"^tv/(?P<tv_show_id>[0-9]+)/recommendations$",
        tv_shows_views.tv_show_recommendations,
        name="recommendations after tv show",
    ),
    re_path(
        r"^tv/(?P<tv_show_id>[0-9]+)/similar$",
        tv_shows_views.similar_tv_shows,
        name="similar tv shows",
    ),
    re_path(
        r"^tv/(?P<tv_show_id>[0-9]+)/providers$",
        tv_shows_views.tv_show_provider,
        name="tv show providers",
    ),
    re_path(r"^tv/genres$", tv_shows_views.tv_show_genres, name="genres for tv shows"),
    re_path(
        r"^tv/with$",
        tv_shows_views.tv_shows_by_genre,
        name="tv shows by genre",
    ),
    re_path(
        r"^tv/(?P<tv_show_id>[0-9]+)/videos$",
        tv_shows_views.tv_show_videos,
        name="tv show videos",
    ),
    re_path(r"^tv/search$", tv_shows_views.search_tv_shows, name="search tv show"),
]
