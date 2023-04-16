from django.http.response import JsonResponse
from rest_framework import status

from ..models.movie_lib_models import Movie
from Authentication.models import User
from Movies_Library_API.serializers import MovieSerializer, Movie_UserSerializer
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Movies_Library_API.movie_db_requests import MovieRequests
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
        data = Movie.users.through.objects.filter(user_id=user_id)

        serializer_movie_user = Movie_UserSerializer(data, many=True)
        return JsonResponse(serializer_movie_user.data, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
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
def movie_details_api(request, movie_id):
    if request.method == "GET":
        data = MovieRequests().get_movie_details(movie_id)

        if data is not None:
            return JsonResponse(data.__dict__(), safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def popular_movies(request):
    if request.method == "GET":
        data = MovieRequests().get_popular_movies()
        data_json = MovieRequests().__convert_movie_list_to_json__(data)

        if data is not None:
            return JsonResponse(data_json, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def upcoming_movies(request):
    if request.method == "GET":
        data = MovieRequests().get_upcoming_movies()
        data_json = MovieRequests().__convert_movie_list_to_json__(data)

        if data is not None:
            return JsonResponse(data_json, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def latest_movies(request):
    if request.method == "GET":
        data = MovieRequests().get_latest_movies()
        data_json = MovieRequests().__convert_movie_list_to_json__(data)

        if data is not None:
            return JsonResponse(data_json, safe=False)

        return JsonResponse(
            {"message": "The movie does not exist"}, status=status.HTTP_404_NOT_FOUND
        )