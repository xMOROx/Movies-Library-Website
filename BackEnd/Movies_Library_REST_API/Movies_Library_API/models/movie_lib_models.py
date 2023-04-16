from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from Authentication.models import User


class Movie(models.Model):
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

    def __str__(self):
        return self.title

    def get_movies_for_user(self, user):
        return self.objects.filter(users=user)

    def __dict__(self):
        return {
            "title": self.title,
            "poster_url": self.poster_url,
            "runtime": self.runtime,
        }


class Actor(models.Model):
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(
        Movie,
        related_name="Movies_Actors",
        through="Movie_Actor",
        through_fields=("actor", "movie"),
        blank=True,
    )

    users = models.ManyToManyField(
        User,
        related_name="Users_Actors",
        through="User_Actor",
        through_fields=("actor", "user"),
        blank=True,
    )

    def __str__(self):
        return self.name

    def __dict__(self):
        return {"name": self.name}


class Movie_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    status = models.CharField(max_length=255, default="Not Watched")
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.user} - {self.movie}"

    def __dict__(self):
        return {
            "user": self.user.__dict__(),
            "movie": self.movie.__dict__(),
            "is_favorite": self.is_favorite,
            "status": self.status,
            "rating": self.rating,
        }


class Movie_Actor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    priority = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.movie} - {self.actor}"

    def __dict__(self):
        return {
            "movie": self.movie.__dict__(),
            "actor": self.actor.__dict__(),
        }


class User_Actor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    status = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.user} - {self.actor}"

    def __dict__(self):
        return {
            "user": self.user.__dict__(),
            "actor": self.actor.__dict__(),
        }
