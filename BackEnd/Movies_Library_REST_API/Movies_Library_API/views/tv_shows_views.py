from Movies_Library_API.serializers import TVShowSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..models.movie_lib_models import TVShow
from ..requests.tv_shows_requests import TVShowsRequests


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_detail(request, tv_show_id):
    try:
        data = TVShow.objects.get(tv_show_id)
    except TVShow.DoesNotExist:
        return JsonResponse(
            {"message": "The tv show does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = TVShowSerializer(data, context={"request": request})
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_details_api(request, tv_show_id):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        data = TVShowsRequests().get_details(tv_show_id, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv show does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def popular_tv_shows(request):
    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        data = TVShowsRequests().get_popular(page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv show do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def upcoming_tv_shows(request):
    if request.method == "GET":
        page = request.GET.get("page", 1)
        time_window = request.GET.get("time_window", "month")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        data = TVShowsRequests().get_upcoming(page, time_window, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def latest_tv_shows(request):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        page = request.GET.get("page", 1)
        region = request.GET.get("region", "US")
        data = TVShowsRequests().get_latest(page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_tv_shows(request):
    if request.method == "GET":
        time_window = request.GET.get("time_window")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        if time_window is None:
            return JsonResponse(
                {"message": "The time window is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = TVShowsRequests().get_trending_by_time(
            time_window, page, language, region
        )

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def airing_today(request):
    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        data = TVShowsRequests().get_airing_today(page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def airing_this_week(request):
    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        data = TVShowsRequests().get_airing_this_week(page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_credits(request, tv_show_id):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        data = TVShowsRequests().get_credits(tv_show_id, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv show does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_recommendations(request, tv_show_id):
    if request.method == "GET":
        page = request.GET.get("page")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        data = TVShowsRequests().get_recommendations(tv_show_id, page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def similar_tv_shows(request, tv_show_id):
    if request.method == "GET":
        page = request.GET.get("page")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        data = TVShowsRequests().get_similar(tv_show_id, page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_provider(request, tv_show_id):
    if request.method == "GET":
        country_code = request.GET.get("CC", "US")
        language = request.GET.get("language", "en-US")
        data = TVShowsRequests().get_provider(tv_show_id, country_code, language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv show does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_genres(request):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        data = TVShowsRequests().get_genres(language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The genres do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_shows_by_genre(request):
    if request.method == "GET":
        genre_ids = request.GET.get("genres", "")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")

        if genre_ids == "":
            data = TVShowsRequests().get_popular(page, language)
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        data = TVShowsRequests().get_content_by_genre(genre_ids, page, language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "Tv shows do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def tv_show_videos(request, tv_show_id):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        data = TVShowsRequests().get_videos(tv_show_id, language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The videos do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def search_tv_shows(request):
    if request.method == "GET":
        query = request.GET.get("query")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        if query is None:
            return JsonResponse(
                {"message": "The query is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = TVShowsRequests().search(query, page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The tv shows do not exist"}, status=status.HTTP_404_NOT_FOUND
        )
