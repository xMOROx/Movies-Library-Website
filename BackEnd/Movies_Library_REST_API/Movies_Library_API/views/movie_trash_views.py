from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models.movie_lib_models import Movie, MovieTrash
from Movies_Library_API.serializers import MovieTrashSerializer
from Authentication.models import User
from Authentication.permissions import IsOwner

from ..requests.movie_db_requests import MovieRequests
from rest_framework.serializers import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def crud_for_movie_inside_trash(request, user_id, movie_id):
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
                {"message": "This movie does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            data = MovieTrash.objects.get(user=user_id, movie=movie_id)
        except MovieTrash.DoesNotExist:
            return JsonResponse(
                {"message": "This movie is not in trash"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MovieTrashSerializer(data)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        movie_requests = MovieRequests()

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            movie_api = movie_requests.get_movie_details(movie_id)
            if movie_api is None:
                return JsonResponse(
                    {"message": "This movie does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                movie = Movie.objects.create(
                    id=movie_api["id"],
                    title=movie_api["title"],
                    poster_url=movie_api["poster_path"],
                    runtime=movie_api["runtime"],
                )
            except (DRFValidationError, DjangoValidationError) as e:
                return JsonResponse(
                    {"message": "The movie could not be added"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            _ = MovieTrash.objects.get(user=user_id, movie=movie_id)
            return JsonResponse(
                {"message": "Movie already in trash"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except MovieTrash.DoesNotExist:
            movie_trash = MovieTrash.objects.create(
                user=user,
                movie=movie
            )
            movie_trash.save()

            serializer = MovieTrashSerializer(movie_trash)

            return JsonResponse(
                serializer.data, status=status.HTTP_201_CREATED, safe=False
            )
    elif request.method == "DELETE":
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

        movie_trash = get_object_or_404(MovieTrash, user=user_id, movie=movie_id)
        movie_trash.delete()
        return JsonResponse(
            None, status=status.HTTP_204_NO_CONTENT, safe=False
        )


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
        show_all = "true" == request.GET.get("all", 1)
        data = get_list_or_404(MovieTrash, user=user_id).order_by("-movie__title")
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(data, request)
        if page is not None and not show_all:
            serializer = MovieTrashSerializer(page, many=True)
            return pagination.get_paginated_response(serializer.data)

        serializer = MovieTrashSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
