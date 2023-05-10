from django.http.response import JsonResponse
from rest_framework import status

from ..models.movie_lib_models import Movie_User, Movie
from Authentication.models import User
from Movies_Library_API.serializers import MovieSerializer, Movie_UserSerializer
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..requests.movie_db_requests import MovieRequests
from Authentication.permissions import IsOwner


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def list_of_details_for_movies_per_user(request, user_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        data = Movie_User.objects.select_related("movie").filter(user_id=user_id)

        serializer = Movie_UserSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def details_of_movie_for_user(request, user_id, movie_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            data = Movie.users.through.objects.get(user_id=user_id, movie_id=movie_id)
        except Exception:
            return JsonResponse(
                {"message": "The movie does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer_movie_user = Movie_UserSerializer(data)
        return JsonResponse(serializer_movie_user.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def movie_detail(request, movie_id):
    try:
        data = Movie.objects.get(movie_id)
    except Movie.DoesNotExist:
        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = MovieSerializer(data, context={"request": request})
        return JsonResponse(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def movie_details_api(request, movie_id):
    if request.method == "GET":
        data = MovieRequests().get_movie_details(movie_id)

        if data is not None:
            return JsonResponse(data, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def popular_movies(request):
    if request.method == "GET":
        page = request.query_params.get("page")

        data = MovieRequests().get_popular_movies(page)

        if data is not None:
            return JsonResponse(data, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def upcoming_movies(request):
    if request.method == "GET":
        page = request.query_params.get("page")
        time_window = request.query_params.get("time")

        data = MovieRequests().get_upcoming_movies(page, time_window)

        if data is not None:
            return JsonResponse(data, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def latest_movies(request):
    if request.method == "GET":
        data = MovieRequests().get_latest_movies()

        if data is not None:
            return JsonResponse(data, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def trending_movies(request):
    if request.method == "GET":
        media_type = request.query_params.get("media")
        time_window = request.query_params.get("time")
        page = request.query_params.get("page")
        if media_type is None:
            return JsonResponse(
                {"message": "The media type is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if time_window is None:
            return JsonResponse(
                {"message": "The time window is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = MovieRequests().get_treding_movie_by_media_and_time(
            media_type, time_window, page
        )

        if data is not None:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse(
            {"message": "The movies does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def now_playing_movies(request):
    if request.method == "GET":
        page = request.query_params.get("page")

        data = MovieRequests().get_now_playing_movies(page)

        if data is not None:
            return JsonResponse(data, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def movie_credits(request, movie_id):
    if request.method == "GET":
        data = MovieRequests().get_movie_credits(movie_id)

        if data is not None:
            return JsonResponse(data, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def movie_recommendations(request, movie_id):
    if request.method == "GET":
        page = request.query_params.get("page")

        data = MovieRequests().get_movie_recommendations(movie_id, page)

        if data is not None:
            return JsonResponse(data, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def similar_movies(request, movie_id):
    if request.method == "GET":
        page = request.query_params.get("page")

        data = MovieRequests().get_similar_movies(movie_id, page)

        if data is not None:
            return JsonResponse(data, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def movie_provider(request, movie_id):
    if request.method == "GET":
        country_code = request.query_params.get("CC")
        data = MovieRequests().get_movie_provider(movie_id, country_code)

        if data is not None:
            return JsonResponse(data, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
