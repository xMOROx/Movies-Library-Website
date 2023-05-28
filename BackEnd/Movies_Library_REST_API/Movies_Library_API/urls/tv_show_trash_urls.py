from django.urls import re_path
from Movies_Library_API.views import tv_show_trash_views

urlpatterns = [
    re_path(
        r"^trash/users/(?P<user_id>[0-9]+)/tv-shows$",
        tv_show_trash_views.get_all_tv_shows,
        name="get all tv shows from trash for user",
    ),
    re_path(
        r"^trash/users/(?P<user_id>[0-9]+)/tv-shows/(?P<tv_show_id>[0-9]+)$",
        tv_show_trash_views.crud_for_tv_show_inside_trash,
        name="get tv show from trash",
    ),
]
