import math

from Movies_Library_API.models.movie_lib_models import TVShow, TVShowTrash
from Movies_Library_API.requests.tv_shows_requests import TVShowsRequests
from Movies_Library_API.serializers import TVShowSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_detail(request, tv_show_id: int) -> JsonResponse:
    """
    This function is used to get details about a tv show from the database.
    :param request: Request object
    :param tv_show_id: TV show id
    :return: JsonResponse with tv show details and status code(200) or error message and status code(404)
    Allow any user to access this view
    """
    try:
        data = TVShow.objects.get(tv_show_id)

    except TVShow.DoesNotExist:
        return JsonResponse(
            {"message": "The tv show does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = TVShowSerializer(data, context={"request": request})

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_details_api(request, tv_show_id: int) -> JsonResponse:
    """
    This function is used to get details about a tv show from the API.
    :param request: Request object
    :param tv_show_id: TV show id
    :return: JsonResponse with tv show details and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        data = TVShowsRequests().get_details(tv_show_id, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv show does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def popular_tv_shows(request) -> JsonResponse:
    """
    This function is used to get popular tv shows from the API.
    :param request: Request object
    :return: JsonResponse with popular tv shows and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = TVShowsRequests().get_popular(page, language, region)

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv show do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def upcoming_tv_shows(request) -> JsonResponse:
    """
    This function is used to get upcoming tv shows from the API.
    :param request: Request object
    :return: JsonResponse with upcoming tv shows and status code(200) or error message and status code(404)
    Allow any user to access this view
    """
    if request.method == "GET":
        page = request.GET.get("page", 1)
        time_window = request.GET.get("time_window", "month")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = TVShowsRequests().get_upcoming(page, time_window, language, region)

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def latest_tv_shows(request) -> JsonResponse:
    """
    This function is used to get latest tv shows from the API.
    :param request: Request object
    :return: JsonResponse with latest tv shows and status code(200) or error message and status code(404)
    Allow any user to access this view
    """
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        page = request.GET.get("page", 1)
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = TVShowsRequests().get_latest(page, language, region)

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_tv_shows(request) -> JsonResponse:
    """
    This function is used to get trending tv shows from the API.
    :param request: Request object
    :return: JsonResponse with trending tv shows and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        time_window = request.GET.get("time_window")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        if time_window is None:
            return JsonResponse(
                {"message": "The time window is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = TVShowsRequests().get_trending_by_time(
            time_window, page, language, region
        )

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def airing_today(request) -> JsonResponse:
    """
    This function is used to get airing today tv shows from the API.
    :param request: Request object
    :return: JsonResponse with airing today tv shows and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = TVShowsRequests().get_airing_today(page, language, region)

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def airing_this_week(request) -> JsonResponse:
    """
    This function is used to get airing this week tv shows from the API.
    :param request: Request object
    :return: JsonResponse with airing this week tv shows and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = TVShowsRequests().get_airing_this_week(page, language, region)

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_credits(request, tv_show_id: int) -> JsonResponse:
    """
    This function is used to get tv show credits from the API.
    :param request: Request object
    :param tv_show_id: The id of the tv show
    :return: JsonResponse with tv show credits and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        data = TVShowsRequests().get_credits(tv_show_id, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv show does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_recommendations(request, tv_show_id: int) -> JsonResponse:
    """
    This function is used to get tv show recommendations from the API.
    :param request: Request object
    :param tv_show_id: The id of the tv show
    :return: JsonResponse with tv show recommendations and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        page = request.GET.get("page")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = TVShowsRequests().get_recommendations(tv_show_id, page, language, region)

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def similar_tv_shows(request, tv_show_id: int) -> JsonResponse:
    """
    This function is used to get similar tv shows from the API.
    :param request: Request object
    :param tv_show_id: The id of the tv show
    :return: JsonResponse with similar tv shows and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        page = request.GET.get("page")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = TVShowsRequests().get_similar(tv_show_id, page, language, region)

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_provider(request, tv_show_id: int) -> JsonResponse:
    """
    This function is used to get tv show providers from the API.
    :param request: Request object
    :param tv_show_id: The id of the tv show
    :return: JsonResponse with tv show providers and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        country_code = request.GET.get("CC", "US")
        language = request.GET.get("language", "en-US")
        data = TVShowsRequests().get_provider(tv_show_id, country_code, language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv show does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_genres(request) -> JsonResponse:
    """
    This function is used to get tv show genres from the API.
    :param request: Request object
    :return: JsonResponse with tv show genres and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        data = TVShowsRequests().get_genres(language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The genres do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_shows_by_genre(request) -> JsonResponse:
    """
    This function is used to get tv shows by genre from the API.
    :param request: Request object
    :return: JsonResponse with tv shows by genre and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        genre_ids = request.GET.get("genres", "")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        user_id = int(request.GET.get("user", -1))

        if genre_ids == "":
            data = TVShowsRequests().get_popular(page, language)
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        data = TVShowsRequests().get_content_by_genre(genre_ids, page, language)

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "Tv shows do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_videos(request, tv_show_id: int) -> JsonResponse:
    """
    This function is used to get tv show videos from the API.
    :param request: Request object
    :param tv_show_id: The id of the tv show
    :return: JsonResponse with tv show videos and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        data = TVShowsRequests().get_videos(tv_show_id, language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The videos do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def search_tv_shows(request) -> JsonResponse:
    """
    This function is used to search tv shows from the API.
    :param request: Request object
    :return: JsonResponse with tv shows and status code(200) or error message and status code(404)
    Allow any user to access this view
    """

    if request.method == "GET":
        query = request.GET.get("query")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        if query is None:
            return JsonResponse(
                {"message": "The query is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = TVShowsRequests().search(query, page, language, region)

        if user_id != -1:
            data = filter_tv_show_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist."}, status=status.HTTP_404_NOT_FOUND
        )


def filter_tv_show_inside_trash(data, user_id):
    """
    This function is used to filter tv shows that are inside the trash.
    :param data:
    :param user_id:
    :return: filter tv shows that are not inside the trash
    """

    trash = TVShowTrash.objects.filter(user_id=user_id)
    counter = 0

    if 'results' not in data:
        return data

    for tv_show in data['results']:
        for trashed_tv_show in trash:
            if tv_show['id'] == trashed_tv_show.tv_show_id:
                counter += 1
                data['results'].remove(tv_show)

    data['total_results'] -= counter
    data['total_pages'] = math.ceil(data['total_results'] / 20)

    return data
