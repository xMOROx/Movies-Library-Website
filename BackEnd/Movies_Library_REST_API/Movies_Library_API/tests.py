from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


# ===================================== Actors =========================================

class GetActorDetailsViewTests(APITestCase):
    valid_actor_id = 123  # ID aktora do testowania
    invalid_actor_id = 14324325  # Nieprawidłowe ID aktora, który nie istnieje

    @transaction.atomic
    def test_get_actor_details(self):
        url = reverse("get actor details", kwargs={"actor_id": self.valid_actor_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_get_actor_details_not_found(self):
        url = reverse("get actor details", kwargs={"actor_id": self.invalid_actor_id})

        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data["message"], "Actor not found.")


class GetActorExternalDataViewTests(APITestCase):
    valid_actor_id = 123  # ID aktora do testowania
    invalid_actor_id = 14324325  # Nieprawidłowe ID aktora, który nie istnieje

    @transaction.atomic
    def test_get_actor_external_data(self):
        url = reverse("get actor external data", kwargs={"actor_id": self.valid_actor_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_get_actor_external_data_not_found(self):
        url = reverse("get actor external data", kwargs={"actor_id": self.invalid_actor_id})

        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data["message"], "Actor not found.")


class GetActorCastViewTests(APITestCase):
    valid_actor_id = 123  # ID aktora do testowania
    invalid_actor_id = 14324325  # Nieprawidłowe ID aktora, który nie istnieje

    @transaction.atomic
    def test_get_actor_cast(self):
        url = reverse("get actor cast", kwargs={"actor_id": self.valid_actor_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_get_actor_cast_not_found(self):
        url = reverse("get actor cast", kwargs={"actor_id": self.invalid_actor_id})

        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data["message"], "Actor not found.")


class GetTrendingActorsViewTests(APITestCase):
    @transaction.atomic
    def test_get_trending_actors(self):
        url = reverse("get trending actors")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetActorsViewTests(APITestCase):
    @transaction.atomic
    def test_get_actors(self):
        url = reverse("get actors")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ===================================== Movies =========================================
class MovieDetailsAPITests(APITestCase):
    valid_movie_id = 123  # ID filmu do testowania
    invalid_movie_id = 14324325  # Nieprawidłowe ID filmu, który nie istnieje

    @transaction.atomic
    def test_movie_details_api(self):
        url = reverse("movie details api", kwargs={"movie_id": self.valid_movie_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_movie_details_api_not_found(self):
        url = reverse("movie details api", kwargs={"movie_id": self.invalid_movie_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PopularMoviesViewTests(APITestCase):
    @transaction.atomic
    def test_popular_movies(self):
        url = reverse("popular movies")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpcomingMoviesViewTests(APITestCase):
    @transaction.atomic
    def test_upcoming_movies(self):
        url = reverse("upcoming movies")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LatestMoviesViewTests(APITestCase):
    @transaction.atomic
    def test_latest_movies(self):
        url = reverse("latest movies")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrendingMoviesViewTests(APITestCase):
    @transaction.atomic
    def test_trending_movies(self):
        url = reverse("trending movies")
        media_type = "MOVIE"  # Zmienić na właściwy typ mediów
        time_window = "WEEK"  # Zmienić na właściwe okno czasowe

        response = self.client.get(url, data={"media": media_type, "time_window": time_window})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_trending_movies_missing_params(self):
        url = reverse("trending movies")

        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["message"], "The media type is required.")

        response = self.client.get(url, data={"media": "MOVIE"})
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["message"], "The time window is required.")


class NowPlayingMoviesViewTests(APITestCase):
    @transaction.atomic
    def test_now_playing_movies(self):
        url = reverse("now playing")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MovieCreditsViewTests(APITestCase):
    valid_movie_id = 123  # ID filmu do testowania
    invalid_movie_id = 14324325  # Nieprawidłowe ID filmu, który nie istnieje

    @transaction.atomic
    def test_movie_credits(self):
        url = reverse("movie credits", kwargs={"movie_id": self.valid_movie_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_movie_credits_not_found(self):
        url = reverse("movie credits", kwargs={"movie_id": self.invalid_movie_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "The movie does not exist.")


class MovieRecommendationsViewTests(APITestCase):
    valid_movie_id = 123  # ID filmu do testowania
    invalid_movie_id = 14324325  # Nieprawidłowe ID filmu, który nie istnieje

    @transaction.atomic
    def test_movie_recommendations(self):
        url = reverse("recommendations after movie", kwargs={"movie_id": self.valid_movie_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

    def test_movie_recommendations_not_found(self):
        url = reverse("recommendations after movie", kwargs={"movie_id": self.invalid_movie_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "The movie does not exist.")


class SimilarMoviesViewTests(APITestCase):
    valid_movie_id = 123  # ID filmu do testowania
    invalid_movie_id = 14324325  # Nieprawidłowe ID filmu, który nie istnieje

    @transaction.atomic
    def test_similar_movies(self):
        url = reverse("similar movies", kwargs={"movie_id": self.valid_movie_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_similar_movies_not_found(self):
        url = reverse("similar movies", kwargs={"movie_id": self.invalid_movie_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "The movie does not exist.")


class MovieProviderViewTests(APITestCase):
    valid_movie_id = 123  # ID filmu do testowania
    invalid_movie_id = 14324325  # Nieprawidłowe ID filmu, który nie istnieje

    @transaction.atomic
    def test_movie_provider(self):
        url = reverse("movie providers", kwargs={"movie_id": self.valid_movie_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_movie_provider_not_found(self):
        url = reverse("movie providers", kwargs={"movie_id": self.invalid_movie_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "The movie does not exist.")


class MovieGenresViewTests(APITestCase):
    @transaction.atomic
    def test_movie_genres(self):
        url = reverse("genres for movies")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MoviesByGenreViewTests(APITestCase):
    valid_genre_ids = 28  # ID gatunków do testowania
    invalid_genre_ids = 123123  # Nieprawidłowe ID gatunków, które nie istnieją

    @transaction.atomic
    def test_movies_by_genre(self):
        url = reverse("movies by genre")

        response = self.client.get(url, {"genres": self.valid_genre_ids})

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MovieVideosViewTests(APITestCase):
    valid_movie_id = 123  # ID filmu do testowania
    invalid_movie_id = 14324325  # Nieprawidłowe ID filmu, który nie istnieje

    @transaction.atomic
    def test_movie_videos(self):
        url = reverse("movie videos", kwargs={"movie_id": self.valid_movie_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_movie_videos_not_found(self):
        url = reverse("movie videos", kwargs={"movie_id": self.invalid_movie_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "The videos does not exist.")


class SearchMoviesViewTests(APITestCase):
    @transaction.atomic
    def test_search_movies(self):
        query = "Action"
        url = reverse("search movies")

        response = self.client.get(url, {"query": query})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_search_movies_no_query(self):
        url = reverse("search movies")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertEqual(response_data["message"], "The query is required.")
