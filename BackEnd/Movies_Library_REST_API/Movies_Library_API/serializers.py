from rest_framework import serializers
from .models.movie_lib_models import Movie, Movie_User, MovieTrash


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ("users",)


class Movie_UserSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    class Meta:
        model = Movie_User
        exclude = ("user",)

    def get_movie(self, obj):
        try:
            obj.movie
        except AttributeError:
            return None
        return MovieSerializer(obj.movie).data


class MovieTrashSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    class Meta:
        model = MovieTrash
        exclude = ("user",)

    def get_movie(self, obj):
        return MovieSerializer(obj.movie).data
