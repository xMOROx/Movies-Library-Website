from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from ..models.movie_lib_models import Movie, Movie_User
from Authentication.models import User
from Movies_Library_API.serializers import Movie_UserSerializer
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from Movies_Library_API.movie_db_requests import MovieRequests
from Authentication.permissions import IsOwner


class AddMovieToUserView(views.APIView):
    permission_classes = [IsAuthenticated & IsOwner]

    def put(self, request, user_id, movie_id):
        movie_user = Movie_User.objects.filter(user=user_id, movie=movie_id).first()

        movie_user_serializer = Movie_UserSerializer(data=request.data)
        movie_user_serializer.is_valid(raise_exception=True)

        # TODO if status "Not watched" delete record from Movie_User
        # TODO if status not "Watched" cannot set is_favorite = True and give rating

        if movie_user is not None:
            try:
                if "rating" in movie_user_serializer.validated_data:
                    movie_user.rating = movie_user_serializer.validated_data["rating"]

                if "is_favorite" in movie_user_serializer.validated_data:
                    movie_user.is_favorite = movie_user_serializer.validated_data["is_favorite"]

                if "status" in movie_user_serializer.validated_data:
                    movie_user.status = movie_user_serializer.validated_data["status"]

                movie_user.save()
                return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)
            except:
                return JsonResponse(
                    {"message": "The movie could not be updated"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        movie_requests = MovieRequests()

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            movie_api = movie_requests.get_movie_details(movie_id)

            if movie_api is None:
                return JsonResponse(
                    {"message": f"The movie with given id {movie_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            try:
                movie = Movie.objects.create(
                    id=movie_api["id"],
                    title=movie_api["original_title"],
                    poster_url=movie_api["poster_path"],
                    runtime=movie_api["runtime"],
                )
            except:
                return JsonResponse(
                    {"message": "The movie could not be added"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if "rating" not in movie_user_serializer.validated_data:
            movie_user_serializer.validated_data["rating"] = None

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
