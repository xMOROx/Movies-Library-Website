from CustomAuthentication.models import User
from CustomAuthentication.permissions import IsOwner
from Movies_Library_API.models.movie_lib_models import Movie, Movie_User
from Movies_Library_API.recommendations_algorithm import (
    collaborative_filtering_recommendation,
)
from Movies_Library_API.requests.movie_requests import MovieRequests
from Movies_Library_API.serializers import Movie_UserSerializer
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    ObjectDoesNotExist,
    MultipleObjectsReturned,
)
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(["PUT"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def add_movie_to_user(request, user_id, movie_id):
    if request.method == "PUT":
        movie_user = Movie_User.objects.filter(user=user_id, movie=movie_id).first()

        try:
            movie_user_serializer = Movie_UserSerializer(data=request.data)
            movie_user_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return JsonResponse(
                {"message": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST
            )

        if movie_user is not None:
            try:
                if "rating" in movie_user_serializer.validated_data:
                    movie_user.rating = movie_user_serializer.validated_data["rating"]

                if "is_favorite" in movie_user_serializer.validated_data:
                    movie_user.is_favorite = movie_user_serializer.validated_data[
                        "is_favorite"
                    ]

                if "status" in movie_user_serializer.validated_data:
                    movie_user.status = movie_user_serializer.validated_data["status"]

                if movie_user.status == "Not watched":
                    movie_user.delete()
                else:
                    movie_user.save()

                return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)
            except (DRFValidationError, DjangoValidationError) as e:
                return JsonResponse(
                    {"message": "The movie could not be updated."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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
                    {"message": f"The movie with given id {movie_id} does not exist."},
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

        if "rating" not in movie_user_serializer.validated_data:
            movie_user_serializer.validated_data["rating"] = 0

        if "is_favorite" not in movie_user_serializer.validated_data:
            movie_user_serializer.validated_data["is_favorite"] = False

        if "status" not in movie_user_serializer.validated_data:
            movie_user_serializer.validated_data["status"] = "Not watched"

        movie_user = Movie_User.objects.create(
            user=user,
            movie=movie,
            rating=movie_user_serializer.validated_data["rating"],
            is_favorite=movie_user_serializer.validated_data["is_favorite"],
            status=movie_user_serializer.validated_data["status"],
        )

        movie_user.save()

        return JsonResponse(
            movie_user_serializer.data, status=status.HTTP_201_CREATED, safe=False
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def list_of_details_for_movies_per_user(request, user_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        show_all = "true" == request.GET.get("all", 1)
        data = (
            Movie_User.objects.select_related("movie")
            .filter(user_id=user_id)
            .order_by("-movie__title")
        )
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(data, request)
        if page is not None and not show_all:
            serializer = Movie_UserSerializer(page, many=True)
            return pagination.get_paginated_response(serializer.data)

        serializer = Movie_UserSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def details_of_movie_for_user(request, user_id, movie_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            data = Movie.users.through.objects.get(user_id=user_id, movie_id=movie_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                {"message": "The movie does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except MultipleObjectsReturned:
            return JsonResponse(
                {"message": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer_movie_user = Movie_UserSerializer(data)
        return JsonResponse(
            serializer_movie_user.data, safe=False, status=status.HTTP_200_OK
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def recommendations(request, user_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        movies = collaborative_filtering_recommendation(user_id)
        movies_serialized = Movie_UserSerializer(movies, many=True)
        data = {"movies": movies_serialized.data}
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
