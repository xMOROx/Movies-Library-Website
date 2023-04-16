from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from ..models.movie_lib_models import Movie
from Authentication.models import User
from Movies_Library_API.serializers import MovieSerializer
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from Movies_Library_API.movie_db_requests import MovieRequests


# Create your views here.
@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def movie_list(request, user_id):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        data = Movie.objects.filter(users=user)

        serializer = MovieSerializer(data, context={"request": request}, many=True)

        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        movie_data = JSONParser().parse(request)
        serializer = MovieSerializer(data=movie_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        count = Movie.objects.all().delete()
        return JsonResponse(
            {"message": "{} Movies were deleted successfully!".format(count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )


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
