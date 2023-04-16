from rest_framework import serializers
from .models.movie_lib_models import Movie, Movie_User


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class Movie_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_User
        fields = ("is_favorite", "status", "rating")
