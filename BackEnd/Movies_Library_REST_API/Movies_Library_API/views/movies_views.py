import math

from Movies_Library_API.models.movie_lib_models import Movie, MovieTrash
from Movies_Library_API.requests.movie_requests import MovieRequests
from Movies_Library_API.serializers import MovieSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_detail(request, movie_id: int) -> JsonResponse:
    """
    Get movie details from database
    Accept language and region as url parameters
    :param request: request
    :param movie_id: movie id
    :return: JsonResponse
    Allowing any user to access this endpoint
    """

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
def movie_details_api(request, movie_id: int) -> JsonResponse:
    """
    Get movie details from API
    Accept language and region as url parameters
    :param request: request
    :param movie_id: movie id - 404 if not found
    :return: JsonResponse with movie details and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

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
def popular_movies(request) -> JsonResponse:
    """
    Get popular movies from API
    Accept page, language and region as url parameters
    :param request: request
    :return: JsonResponse with popular movies and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = MovieRequests().get_popular(page, language, region)
        if user_id != -1:
            data = filter_movie_inside_trash(data, user_id)

        data = filter_movie_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def upcoming_movies(request) -> JsonResponse:
    """
    Get upcoming movies from API.
    Accept time_window parameter with values week, month as url parameters
    Accept page, language and region as url parameters
    :param request: request
    :return: JsonResponse with upcoming movies and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

    if request.method == "GET":
        page = request.GET.get("page", 1)
        time_window = request.GET.get("time_window", "month")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = MovieRequests().get_upcoming(page, time_window, language, region)

        if user_id != -1:
            data = filter_movie_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def latest_movies(request) -> JsonResponse:
    """
    Get latest movies from API
    Accept page, language and region as url parameters
    :param request: request
    :return: JsonResponse with latest movies and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

    if request.method == "GET":
        language = request.GET.get("language", "en-US")
        page = request.GET.get("page", 1)
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = MovieRequests().get_latest(page, language, region)
        if user_id != -1:
            data = filter_movie_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie do not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_movies(request) -> JsonResponse:
    """
    Get trending movies from API
    Accept time_window parameter with values day, week as url parameters
    Accept page, language and region as url parameters
    :param request: request
    :return: JsonResponse with trending movies and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

    if request.method == "GET":
        time_window = request.GET.get("time_window")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        if time_window is None:
            return JsonResponse(
                {"message": "The time window is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = MovieRequests().get_trending_by_time(time_window, page, language, region)

        if user_id != -1:
            data = filter_movie_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movies does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def now_playing_movies(request) -> JsonResponse:
    """
    Get now playing movies from API
    Accept page, language and region as url parameters
    :param request: request
    :return: JsonResponse with now playing movies and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

    if request.method == "GET":
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = MovieRequests().get_now_playing(page, language, region)

        if user_id != -1:
            data = filter_movie_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_credits(request, movie_id: int) -> JsonResponse:
    """
    Get movie credits from API
    Accept language and region as url parameters
    :param request: request
    :param movie_id: movie id
    :return: JsonResponse with movie credits and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

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
def movie_recommendations(request, movie_id: int) -> JsonResponse:
    """
    Get movie recommendations from API
    Accept page, language and region as url parameters
    :param request: request
    :param movie_id: movie id
    :return: JsonResponse with movie recommendations and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

    if request.method == "GET":
        page = request.GET.get("page")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = MovieRequests().get_recommendations(movie_id, page, language, region)

        if user_id != -1:
            data = filter_movie_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def similar_movies(request, movie_id: int) -> JsonResponse:
    """
    Get similar movies from API
    Accept page, language and region as url parameters
    :param request: request
    :param movie_id: movie id
    :return: JsonResponse with similar movies and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

    if request.method == "GET":
        page = request.GET.get("page")
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user_id = int(request.GET.get("user", -1))

        data = MovieRequests().get_similar(movie_id, page, language, region)

        if user_id != -1:
            data = filter_movie_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movie does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_provider(request, movie_id: int) -> JsonResponse:
    """
    Get movie providers from API
    Accept country code and language as url parameters
    :param request: request
    :param movie_id: movie id
    :return: JsonResponse with movie providers and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

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
def movie_genres(request) -> JsonResponse:
    """
    Get movie genres from API
    Accept language as url parameters
    :param request: request
    :return: JsonResponse with movie genres and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

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
def movies_by_genre(request) -> JsonResponse:
    """
    Get movies by genre from API
    Accept genre ids, page and language as url parameters
    :param request: request
    :return: JsonResponse with movies by genre and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

    if request.method == "GET":
        genre_ids = request.GET.get("genres", "")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        user_id = int(request.GET.get("user", -1))

        if genre_ids == "":
            data = MovieRequests().get_popular(page, language)
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        data = MovieRequests().get_content_by_genre(genre_ids, page, language)

        if user_id != -1:
            data = filter_movie_inside_trash(data, user_id)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movies does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_videos(request, movie_id: int) -> JsonResponse:
    """
    Get movie videos from API
    Accept language as url parameters
    :param request: request
    :param movie_id: movie id
    :return: JsonResponse with movie videos and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

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
def search_movies(request) -> JsonResponse:
    """
    Search movies from API
    Accept query, page, language and region as url parameters
    :param request: request
    :return: JsonResponse with movies and status code(200) or error message and status code(404)
    Allowing any user to access this endpoint
    """

    if request.method == "GET":
        query = request.GET.get("query")
        page = request.GET.get("page", 1)
        language = request.GET.get("language", "en-US")
        region = request.GET.get("region", "US")
        user = int(request.GET.get("user", -1))

        if query is None:
            return JsonResponse(
                {"message": "The query is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = MovieRequests().search(query, page, language, region)

        if user != -1:
            data = filter_movie_inside_trash(data, user)

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movies does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


def filter_movie_inside_trash(data: dict, user_id: int) -> dict:
    """
    Filter movies inside user trash
    :param data
    :param user_id
    :return: filter movies that are not inside user trash
    """

    trash = MovieTrash.objects.filter(user_id=user_id)
    counter = 0

    if "result" not in data:
        return data

    for movie in data["results"]:
        for trashed_movie in trash:
            if movie["id"] == trashed_movie.movie_id:
                counter += 1
                data["results"].remove(movie)

    data["total_results"] -= counter
    data["total_pages"] = math.ceil(data["total_results"] / 20)

    return data
