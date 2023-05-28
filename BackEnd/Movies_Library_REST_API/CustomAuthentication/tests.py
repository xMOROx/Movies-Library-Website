from CustomAuthentication.models import User
from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


# ==================== Create user ====================

class UserTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'testpassword',
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(**self.user_data)
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


# ==================== Create user ====================

# ==================== Admin views ====================
class UserListViewTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="adminpassword"
        )
        self.client.force_authenticate(user=self.admin_user)

    @transaction.atomic
    def test_get_user_list(self):
        url = reverse("admin users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateUserViewTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="adminpassword"
        )
        self.client.force_authenticate(user=self.admin_user)
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="old_password"
        )
        self.url = reverse("admin update user", args=[self.user.id])

    @transaction.atomic
    def test_update_user(self):
        data = {
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "email": "new_email@example.com"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated First Name")
        self.assertEqual(self.user.last_name, "Updated Last Name")
        self.assertEqual(self.user.email, "new_email@example.com")

    @transaction.atomic
    def test_update_user_invalid_email(self):
        User.objects.create(email="test@example.com")
        data = {
            "email": "test@example.com"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @transaction.atomic
    def test_update_user_not_found(self):
        non_existent_user_id = 9999
        url = reverse("admin update user", args=[non_existent_user_id])
        data = {
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "email": "new_email@example.com"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ChangePasswordForUserViewTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="adminpassword"
        )
        self.client.force_authenticate(user=self.admin_user)
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="old_password"
        )
        self.url = reverse("admin change password", args=[self.user.id])

    @transaction.atomic  # TODO: repair test
    def test_change_password(self):
        data = {
            "new_password": "changed_password"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("changed_password"))

    @transaction.atomic
    def test_change_password_invalid_data(self):
        data = {
            "new_password": ""
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password("new_password"))


# ==================== Admin views ====================


# ==================== User views ====================
class UserRegisterViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @transaction.atomic
    def test_register_user(self):
        url = reverse("register")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "password123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("User id" in response.data)
        self.assertEqual(response.data["message"], "User created successfully")

    @transaction.atomic
    def test_register_user_duplicate_email(self):
        User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            password="password123",
        )
        url = reverse("register")
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "password456",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["message"], "Email already exists")


class UserViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            password="password123",
        )
        self.client = APIClient()
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(self.access_token)}")

    @transaction.atomic
    def test_get_user(self):
        url = reverse("users", kwargs={"user_id": self.user.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)
        self.assertEqual(response.data["email"], self.user.email)

    @transaction.atomic
    def test_update_user(self):
        url = reverse("users", kwargs={"user_id": self.user.id})
        data = {
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "email": "updatedemail@example.com",
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated First Name")
        self.assertEqual(self.user.last_name, "Updated Last Name")
        self.assertEqual(self.user.email, "updatedemail@example.com")

    @transaction.atomic
    def test_delete_user(self):
        url = reverse("users", kwargs={"user_id": self.user.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class ChangePasswordViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            password="password123",
        )
        self.client.force_authenticate(user=self.user)
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(self.access_token)}")

    @transaction.atomic
    def test_change_password(self):
        url = reverse("change password", kwargs={"user_id": self.user.id})
        data = {
            "password": "password123",
            "new_password": "new_password",
            "confirm_password": "new_password",
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_password"))

    @transaction.atomic
    def test_change_password_incorrect_current_password(self):
        url = reverse("change password", kwargs={"user_id": self.user.id})
        data = {
            "password": "incorrect_password",
            "new_password": "new_password",
            "confirm_password": "new_password",
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["message"], "Your old password was entered incorrectly. Please enter it again.")

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("password123"))

    @transaction.atomic
    def test_change_password_passwords_not_matching(self):
        url = reverse("change password", kwargs={"user_id": self.user.id})
        data = {
            "password": "password123",
            "new_password": "new_password",
            "confirm_password": "different_password",
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["message"], "The two password fields didn't match.")

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("password123"))

# ==================== User views ====================
