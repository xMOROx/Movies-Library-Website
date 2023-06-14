from CustomAuthentication.models import User
from CustomAuthentication.utils.permissions import IsOwner
from Movies_Library_API.models.movie_lib_models import Movie, MovieTrash
from Movies_Library_API.requests.movie_requests import MovieRequests
from Movies_Library_API.serializers import MovieTrashSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
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
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def crud_for_movie_inside_trash(request, user_id: int, movie_id: int) -> JsonResponse:
    """
    CRUD for movie inside trash
    :param request: request object
    :param user_id: user id
    :param movie_id: movie id
    :return: JsonResponse with movies inside trash and status code(200, 201, 204)
    or error message with status code(400, 404)
    Allowing only authenticated users to access this view and only the owner of the movie inside his trash or superuser
    """

    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return JsonResponse(
                {"message": "The user does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            _ = Movie.objects.get(pk=movie_id)

        except Movie.DoesNotExist:
            return JsonResponse(
                {"message": "The movie does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            data = MovieTrash.objects.get(user=user_id, movie=movie_id)

        except MovieTrash.DoesNotExist:

            return JsonResponse(
                {"message": "The movie is not in trash"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MovieTrashSerializer(data)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == "POST":
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        movie_requests = MovieRequests()

        try:
            movie = Movie.objects.get(pk=movie_id)

        except Movie.DoesNotExist:
            movie_api = movie_requests.get_details(movie_id)

            if movie_api is None:
                return JsonResponse(
                    {"message": "The movie does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            try:
                movie = Movie.objects.create(
                    id=movie_api["id"],
                    title=movie_api["title"],
                    poster_url=movie_api["poster_path"],
                    runtime=movie_api["runtime"],
                )

            except (DRFValidationError, DjangoValidationError):
                return JsonResponse(
                    {"message": "The movie could not be added."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            _ = MovieTrash.objects.get(user=user_id, movie=movie_id)

            return JsonResponse(
                {"message": "Movie already in trash."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except MovieTrash.DoesNotExist:
            movie_trash = MovieTrash.objects.create(user=user, movie=movie)
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
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            _ = Movie.objects.get(pk=movie_id)

        except Movie.DoesNotExist:
            return JsonResponse(
                {"message": "The movie does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        movie_trash = get_object_or_404(MovieTrash, user=user_id, movie=movie_id)
        movie_trash.delete()

        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def get_all_movies(request, user_id: int) -> JsonResponse:
    """
    Get all movies from trash
    :param request: request object
    :param user_id: user id
    :return: JsonResponse with movies inside trash and status code(200) or error message with status code(404)
    Allowing only authenticated users to access this view and only the owner of the trash or superuser
    """

    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        show_all = "true" == request.GET.get("all", 1)

        data = get_list_or_404(
            MovieTrash.objects.order_by("-movie__title"), user=user_id
        )

        pagination = PageNumberPagination()

        page = pagination.paginate_queryset(data, request)

        if page is not None and not show_all:
            serializer = MovieTrashSerializer(page, many=True)

            return pagination.get_paginated_response(serializer.data)

        serializer = MovieTrashSerializer(data, many=True)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
