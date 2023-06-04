from Movies_Library_API.models.movie_lib_models import (
    Movie,
    Movie_User,
    MovieTrash,
    TVShow,
    TVShow_User,
    TVShowTrash,
)
from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model
    """

    class Meta:
        model = Movie
        exclude = ("users",)


class TVShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVShow
        exclude = ("users",)


class Movie_UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie_User model
    """

    movie = serializers.SerializerMethodField()

    class Meta:
        model = Movie_User
        exclude = ("user",)

    def get_movie(self, obj) -> dict | None:
        try:
            obj.movie
        except AttributeError:
            return None
        return MovieSerializer(obj.movie).data


class RecommendedMovies_UserSerializer(serializers.ModelSerializer):
    """
    Serializer for RecommendedMovies_User model (used for recommendations algorithm)
    """

    movie = serializers.SerializerMethodField()

    class Meta:
        model = Movie_User
        exclude = ("user", "rating", "is_favorite", "status")

    def get_movie(self, obj) -> dict | None:
        try:
            obj.movie
        except AttributeError:
            return None
        return MovieSerializer(obj.movie).data


class TVShow_UserSerializer(serializers.ModelSerializer):
    """
    Serializer for TVShow_User model
    """

    tv_show = serializers.SerializerMethodField()

    class Meta:
        model = TVShow_User
        exclude = ("user",)

    def get_tv_show(self, obj) -> dict | None:
        try:
            obj.tv_show
        except AttributeError:
            return None
        return TVShowSerializer(obj.tv_show).data


class MovieTrashSerializer(serializers.ModelSerializer):
    """
    Serializer for MovieTrash model
    """
    movie = serializers.SerializerMethodField()

    class Meta:
        model = MovieTrash
        exclude = ("user",)

    def get_movie(self, obj) -> dict | None:
        try:
            obj.movie
        except AttributeError:
            return None
        return MovieSerializer(obj.movie).data


class TVShowTrashSerializer(serializers.ModelSerializer):
    """
    Serializer for TVShowTrash model
    """
    tv_show = serializers.SerializerMethodField()

    class Meta:
        model = TVShowTrash
        exclude = ("user",)

    def get_tv_show(self, obj) -> dict | None:
        try:
            obj.tv_show
        except AttributeError:
            return None
        return TVShowSerializer(obj.tv_show).data
