from django.urls import re_path
from ..views import actors_views

urlpatterns = [
    re_path(r"^actors/(?P<actor_id>\d+)$", actors_views.get_actor_details),
    re_path(
        r"^actors/(?P<actor_id>\d+)/external_data$",
        actors_views.get_actor_external_data,
    ),
    re_path(r"^actors/(?P<actor_id>\d+)/cast$", actors_views.get_actor_cast),
]
