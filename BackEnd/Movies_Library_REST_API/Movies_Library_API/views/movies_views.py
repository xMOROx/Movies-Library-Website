from Movies_Library_API.models.movie_lib_models import Movie
from Movies_Library_API.requests.movie_db_requests import MovieRequests
from Movies_Library_API.serializers import MovieSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_detail(request, movie_id):
    try:
        data = Movie.objects.get(movie_id)
    except Movie.DoesNotExist:
        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = MovieSerializer(data, context={"request": request})
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_details_api(request, movie_id):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        data = MovieRequests().get_details(movie_id, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def popular_movies(request):
    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        data = MovieRequests().get_popular(page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def upcoming_movies(request):
    if request.method == "GET":
        page = request.GET.get("page", 1)
        time_window = request.GET.get("time_window", "month")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        data = MovieRequests().get_upcoming(page, time_window, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def latest_movies(request):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        page = request.GET.get("page", 1)
        region = request.GET.get("region", "US")
        data = MovieRequests().get_latest(page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_movies(request):
    if request.method == "GET":
        time_window = request.GET.get("time_window")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        if time_window is None:
            return JsonResponse(
                {"message": "The time window is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = MovieRequests().get_trending_by_time(time_window, page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movies does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def now_playing_movies(request):
    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        data = MovieRequests().get_now_playing(page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_credits(request, movie_id):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        data = MovieRequests().get_credits(movie_id, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_recommendations(request, movie_id):
    if request.method == "GET":
        page = request.GET.get("page")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        data = MovieRequests().get_recommendations(movie_id, page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def similar_movies(request, movie_id):
    if request.method == "GET":
        page = request.GET.get("page")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        data = MovieRequests().get_similar(movie_id, page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_provider(request, movie_id):
    if request.method == "GET":
        country_code = request.GET.get("CC", "US")
        language = request.GET.get("language", "en-US")
        data = MovieRequests().get_provider(movie_id, country_code, language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_genres(request):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        data = MovieRequests().get_genres(language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The genres does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def movies_by_genre(request):
    if request.method == "GET":
        genre_ids = request.GET.get("genres", "")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")

        if genre_ids == "":
            data = MovieRequests().get_popular(page, language)
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        data = MovieRequests().get_content_by_genre(genre_ids, page, language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movies does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_videos(request, movie_id):
    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        data = MovieRequests().get_videos(movie_id, language)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The videos does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def search_movies(request):
    if request.method == "GET":
        query = request.GET.get("query")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")

        if query is None:
            return JsonResponse(
                {"message": "The query is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = MovieRequests().search(query, page, language, region)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movies does not exist."}, status=status.HTTP_404_NOT_FOUND
        )
