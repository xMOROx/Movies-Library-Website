from CustomAuthentication.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CharField


class TVShow(models.Model):
    """
    TVShow model class
    """
    title = models.CharField(max_length=255)
    poster_url = models.CharField(max_length=255, null=True)

    users = models.ManyToManyField(
        User,
        related_name="TVShows_Users",
        through="TVShow_User",
        through_fields=("tv_show", "user"),
        blank=True,
    )

    def __str__(self) -> CharField:
        return self.title

    def get_tv_shows_for_user(self, user: User) -> models.QuerySet:
        return self.objects.filter(users=user)


class Movie(models.Model):
    """
    Movie model class
    """
    title = models.CharField(max_length=255)
    poster_url = models.CharField(max_length=255, null=True)
    runtime = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(500)]
    )

    users = models.ManyToManyField(
        User,
        related_name="Movies_Users",
        through="Movie_User",
        through_fields=("movie", "user"),
        blank=True,
    )

    def __str__(self) -> CharField:
        return self.title

    def get_movies_for_user(self, user: User) -> models.QuerySet:
        return self.objects.filter(users=user)

    class Meta:
        app_label = "Movies_Library_API"


class Actor(models.Model):
    """
    Actor model class
    """
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(
        Movie,
        related_name="Movies_Actors",
        through="Movie_Actor",
        through_fields=("actor", "movie"),
        blank=True,
    )

    tv_shows = models.ManyToManyField(
        TVShow,
        related_name="TVShows_Actors",
        through="TVShow_Actor",
        through_fields=("actor", "tv_show"),
        blank=True
    )

    users = models.ManyToManyField(
        User,
        related_name="Users_Actors",
        through="User_Actor",
        through_fields=("actor", "user"),
        blank=True,
    )

    def __str__(self) -> CharField:
        return self.name


class Movie_User(models.Model):
    """
    Movie_User model class
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    is_favorite = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(
        max_length=255, default="Not Watched", null=True, blank=True
    )
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.user} - {self.movie}"


class TVShow_User(models.Model):
    """
    TVShow_User model class
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)

    is_favorite = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(
        max_length=255, default="Not Watched", null=True, blank=True
    )
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.user} - {self.tv_show}"


class Movie_Actor(models.Model):
    """
    Movie_Actor model class
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    priority = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self) -> str:
        return f"{self.movie} - {self.actor}"


class TVShow_Actor(models.Model):
    """
    TVShow_Actor model class
    """
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    priority = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self) -> str:
        return f"{self.tv_show} - {self.actor}"


class User_Actor(models.Model):
    """
    User_Actor model class
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    status = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self) -> str:
        return f"{self.user} - {self.actor}"


class MovieTrash(models.Model):
    """
    MovieTrash model class
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} - {self.movie}"


class TVShowTrash(models.Model):
    """
    TVShowTrash model class
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} - {self.tv_show}"
