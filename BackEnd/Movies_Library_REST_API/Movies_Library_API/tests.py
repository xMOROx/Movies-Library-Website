from CustomAuthentication.models import User
from Movies_Library_API.models.movie_lib_models import Movie
from django.db import transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
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


# ======================== Admin view ========================
class AdminUserListViewTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="admin@localhost",
            password="admin123",
            first_name="Admin",
            last_name="Admin",
        )
        self.client.login(email="admin@localhost", password="admin123")

    @transaction.atomic
    def test_admin_user_list_view(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse("admin users")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_admin_user_list_view_unauthorized(self):
        self.client.logout()
        url = reverse("admin users")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminUserUpdateViewTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="admin@localhost",
            password="admin123",
            first_name="Admin",
            last_name="Admin",
        )
        self.user = User.objects.create_user(
            email="user@localhost",
            password="user123",
            first_name="User",
            last_name="User",
        )
        self.client.login(email="admin@localhost", password="admin123")
        self.client.force_authenticate(user=self.superuser)

    @transaction.atomic
    def test_admin_user_update_view(self):
        user_id = self.user.id
        url = reverse("admin update user", kwargs={"user_id": user_id})

        response = self.client.patch(url, {"email": "new_email@example.com"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_admin_user_update_view_not_found(self):
        user_id = 123456
        url = reverse("admin update user", kwargs={"user_id": user_id})

        response = self.client.patch(url, {"email": "new_email@example.com"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "User does not exist.")

    @transaction.atomic
    def test_admin_user_update_view_unauthorized(self):
        self.client.logout()
        user_id = self.user.id
        url = reverse("admin update user", kwargs={"user_id": user_id})

        response = self.client.patch(url, {"email": "new_email@example.com"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_admin_user_delete_view(self):
        user_id = self.user.id
        url = reverse("admin update user", kwargs={"user_id": user_id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_admin_user_delete_view_not_found(self):
        user_id = 123456
        url = reverse("admin update user", kwargs={"user_id": user_id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "User does not exist.")


class BanUserViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@localhost",
            password="admin123",
            first_name="Admin",
            last_name="Admin",
        )

        self.unbanned_user = User.objects.create_user(
            email="user@localhost",
            password="user123",
            first_name="User",
            last_name="User",
        )

        self.banned_user = User.objects.create_user(
            email="banned_user@localhost",
            password="user123",
            first_name="Banned",
            last_name="User",
            is_banned=True,
        )

        self.client.login(email="admin@localhost", password="admin123")
        self.client.force_authenticate(user=self.admin)

    @transaction.atomic
    def test_ban_user_view(self):
        user_id = self.unbanned_user.id
        url = reverse("admin ban user", kwargs={"user_id": user_id})

        response = self.client.patch(url, {"is_banned": True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_ban_user_view_not_found(self):
        user_id = 123456
        url = reverse("admin ban user", kwargs={"user_id": user_id})

        response = self.client.patch(url, {"is_banned": True})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "User does not exist.")

    @transaction.atomic
    def test_ban_user_view_multiple_fields(self):
        user_id = self.unbanned_user.id
        url = reverse("admin ban user", kwargs={"user_id": user_id})

        response = self.client.patch(url, {"is_banned": True, "email": "new_email@example.com"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(response_data["message"],
                         "You can't change other fields from here. Use /api/v1/auth/users/{id}/ endpoint.")

    @transaction.atomic
    def test_ban_user_view_already_banned(self):
        user_id = self.banned_user.id
        url = reverse("admin ban user", kwargs={"user_id": user_id})

        response = self.client.patch(url, {"is_banned": True})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertEqual(response_data["message"], "User is already banned.")

    @transaction.atomic
    def test_unban_user_view(self):
        user_id = self.banned_user.id
        url = reverse("admin ban user", kwargs={"user_id": user_id})

        response = self.client.patch(url, {"is_banned": False})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_unban_user_view_already_unbanned(self):
        user_id = self.unbanned_user.id
        url = reverse("admin ban user", kwargs={"user_id": user_id})

        response = self.client.patch(url, {"is_banned": False})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(response_data["message"], "User is already unbanned.")


# =============================================== Users views ==============================================================

class AddMovieToUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@localhost",
            password="user123",
            first_name="User",
            last_name="User",
        )
        self.movie = Movie.objects.create(
            title="Test movie",
            poster_url="https://www.google.com",
            runtime=120,
        )

        self.movie_id = self.movie.id
        self.client = APIClient()
        self.client.login(email="user@localhost", password="user123")
        self.client.force_authenticate(user=self.user)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(self.access_token)}")

    @transaction.atomic
    def test_add_movie_to_existing_user(self):
        url = reverse('add movie to user', kwargs={'user_id': self.user.id, 'movie_id': self.movie_id})

        data = {
            "rating": 4,
            "is_favorite": True,
            "status": "Watched"
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_add_movie_to_nonexistent_user(self):
        url = reverse('add movie to user', kwargs={'user_id': 999, 'movie_id': self.movie_id})
        admin = User.objects.create_superuser(
            email="admin@localhost",
            password="admin123",
            first_name="Admin",
            last_name="Admin",
        )
        self.client.login(email="admin@localhost", password="admin123")
        self.client.force_authenticate(user=admin)

        data = {
            "rating": 3,
            "is_favorite": False,
            "status": "Not watched"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "User does not exist.")

    @transaction.atomic
    def test_add_movie_with_no_permission(self):
        url = reverse('add movie to user', kwargs={'user_id': 999, 'movie_id': self.movie_id})

        data = {
            "rating": 3,
            "is_favorite": False,
            "status": "Not watched"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "You do not have permission to perform this action.")

    @transaction.atomic
    def test_add_movie_with_invalid_data(self):
        url = reverse('add movie to user', kwargs={'user_id': self.user.id, 'movie_id': self.movie_id})
        data = {
            "rating": "invalid",
            "is_favorite": "invalid",
            "status": "Invalid status"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Invalid data.")


class ListOfDetailsForMoviesPerUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@localhost",
            password="user123",
            first_name="User",
            last_name="User",
        )
        self.client = APIClient()
        self.client.login(email="user@localhost", password="user123")
        self.client.force_authenticate(user=self.user)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(self.access_token)}")

    @transaction.atomic
    def test_list_movies_per_existing_user(self):
        url = reverse('details of user movies', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_list_movies_per_nonexistent_user(self):
        url = reverse('details of user movies', kwargs={'user_id': 999})
        admin = User.objects.create_superuser(
            email="admin@localhost",
            password="admin123",
            first_name="Admin",
            last_name="Admin",
        )
        self.client.force_authenticate(user=admin)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "User does not exist.")

    @transaction.atomic
    def test_list_movies_with_no_permission(self):
        url = reverse('details of user movies', kwargs={'user_id': 999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "You do not have permission to perform this action.")


class DetailsOfMovieForUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@localhost",
            password="user123",
            first_name="User",
            last_name="User",
        )

        self.movie = Movie.objects.create(
            title="Test movie",
            poster_url="https://www.google.com",
            runtime=120,
        )
        self.movie_id = self.movie.id

        self.client = APIClient()
        self.client.login(email="user@localhost", password="user123")
        self.client.force_authenticate(user=self.user)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(self.access_token)}")

        url = reverse('add movie to user', kwargs={'user_id': self.user.id, 'movie_id': self.movie_id})

        data = {
            "rating": 4,
            "is_favorite": True,
            "status": "Watched"
        }

        _ = self.client.put(url, data)

    @transaction.atomic
    def test_details_of_existing_movie_for_user(self):
        url = reverse('details of movie for user', kwargs={'user_id': self.user.id, 'movie_id': self.movie_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_details_of_nonexistent_movie_for_user(self):
        url = reverse('details of movie for user', kwargs={'user_id': self.user.id, 'movie_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "The movie does not exist.")

    @transaction.atomic
    def test_details_with_invalid_user(self):
        url = reverse('details of movie for user', kwargs={'user_id': 999, 'movie_id': self.movie_id})
        admin = User.objects.create_superuser(
            email="admin@localhost",
            password="admin123",
            first_name="Admin",
            last_name="Admin",
        )
        self.client.force_authenticate(user=admin)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data["message"], "User does not exist.")

    @transaction.atomic
    def test_details_with_no_permissions(self):
        url = reverse('details of movie for user', kwargs={'user_id': 999, 'movie_id': self.movie_id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "You do not have permission to perform this action.")
# =============================================== Movies trash views ==============================================================
