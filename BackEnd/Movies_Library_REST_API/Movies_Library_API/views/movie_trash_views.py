from django.http.response import JsonResponse

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models.movie_lib_models import Movie, MovieTrash
from Movies_Library_API.serializers import MovieTrashSerializer
from Authentication.models import User
from Authentication.permissions import IsOwner


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def get_movie_by_id(request, user_id, movie_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            _ = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse(
                {"message": "This movie does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        data = MovieTrash.objects.get(user=user_id, movie=movie_id)
        serializer = MovieTrashSerializer(data)
        return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def get_all_movies(request, user_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        data = MovieTrash.objects.filter(user=user_id)
        serializer = MovieTrashSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def add_movie_to_trash(request, user_id, movie_id):
    if request.method == "POST":
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse(
                {"message": "This movie does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        movie_trash = MovieTrash.objects.create(
            user=user,
            movie=movie
        )
        movie_trash.save()

        serializer = MovieTrashSerializer(movie_trash)

        return JsonResponse(
            serializer.data, status=status.HTTP_201_CREATED, safe=False
        )



@api_view(["DELETE"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def delete_movie_from_trash(request, user_id, movie_id):
    if request.method == "POST":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            _ = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse(
                {"message": "This movie does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        movie_trash = MovieTrash.objects.get(user=user_id, movie=movie_id)
        movie_trash.delete()

        return JsonResponse(
            None, status=status.HTTP_204_NO_CONTENT, safe=False
        )
