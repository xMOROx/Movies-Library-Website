from rest_framework import serializers
from .models.movie_lib_models import Movie, Movie_User, MovieTrash, TVShow_User, TVShowTrash


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ("users",)


class TVShowSerializer(serializers.ModelSerializer):
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


class TVShow_UserSerializer(serializers.ModelSerializer):
    tv_show = serializers.SerializerMethodField()

    class Meta:
        model = TVShow_User
        exclude = ("user",)

    def get_tv_show(self, obj):
        try:
            obj.tv_show
        except AttributeError:
            return None
        return TVShowSerializer(obj.tv_show).data


class MovieTrashSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    class Meta:
        model = MovieTrash
        exclude = ("user",)

    def get_movie(self, obj):
        try:
            obj.movie
        except AttributeError:
            return None
        return MovieSerializer(obj.movie).data


class TVShowTrashSerializer(serializers.ModelSerializer):
    tv_show = serializers.SerializerMethodField()

    class Meta:
        model = TVShowTrash
        exclude = ("user",)

    def get_tv_show(self, obj):
        try:
            obj.tv_show
        except AttributeError:
            return None
        return TVShowSerializer(obj.tv_show).data

