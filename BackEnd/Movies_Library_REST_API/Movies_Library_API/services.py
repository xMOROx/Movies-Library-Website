import dataclasses
import datetime
import jwt

from django.conf import settings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User
from . import models


@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    password: str = None
    id: int = None

    @classmethod
    def from_internal(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            id=user.id,
        )


def create_user(user_data_class: "UserDataClass") -> "UserDataClass":
    instance = models.User(
        first_name=user_data_class.first_name,
        last_name=user_data_class.last_name,
        email=user_data_class.email,
    )

    if user_data_class.password:
        instance.set_password(user_data_class.password)

    instance.save()

    return UserDataClass.from_internal(instance)


def user_email_selector(email: str) -> "User":
    user = models.User.objects.filter(email=email).first()
    return user if user else None


def create_token(user_id: int) -> str:
    payload = dict(
        user_id=user_id,
        exp=datetime.datetime.utcnow()
        + datetime.timedelta(hours=int(settings.JWT_EXPIRATION_TIME)),
        iat=datetime.datetime.utcnow(),
    )
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    return token
