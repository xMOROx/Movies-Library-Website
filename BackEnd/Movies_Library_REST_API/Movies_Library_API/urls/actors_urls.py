from Movies_Library_API.views import actors_views
from django.urls import re_path

urlpatterns = [
    re_path(r"^actors/(?P<actor_id>\d+)$", actors_views.get_actor_details, name="get actor details"),
    re_path(
        r"^actors/(?P<actor_id>\d+)/external_data$",
        actors_views.get_actor_external_data, name="get actor external data"
    ),
    re_path(r"^actors/(?P<actor_id>\d+)/cast$", actors_views.get_actor_cast, name="get actor cast"),
    re_path(r"^actors/trending/$", actors_views.get_trending_actors, name="get trending actors"),
    re_path(r"^actors/$", actors_views.get_actors, name="get actors"),
]
