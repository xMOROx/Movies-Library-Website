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

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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