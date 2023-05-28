from django.db import models

from django.contrib.auth import models as auth_models


class UserManager(auth_models.BaseUserManager):
    def create_user(
            self,
            email: str,
            first_name: str,
            last_name: str,
            password: str = None,
            is_active: bool = True,
            is_staff: bool = False,
            is_superuser: bool = False,
            is_banned: bool = False,
    ) -> "User":
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.last_name = last_name

        user.set_password(password)

        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_banned = is_banned

        user.save(using=self._db)

        return user

    def create_superuser(
            self, email: str, first_name: str, last_name: str, password: str = None
    ) -> "User":
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_superuser=True,
        )

        user.save(using=self._db)

        return user

    def create_staffuser(
            self, email: str, first_name: str, last_name: str, password: str = None
    ) -> "User":
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_superuser=False,
        )

        user.save(using=self._db)

        return user

    class Meta:
        app_label = 'CustomAuthentication'


class User(auth_models.AbstractUser):
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_banned = models.BooleanField(default=False)
    username = None
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'CustomAuthentication'
