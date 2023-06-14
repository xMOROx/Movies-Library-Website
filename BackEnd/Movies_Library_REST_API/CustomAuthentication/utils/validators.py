from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def validate_email(email: str) -> None:
    """
        Validate email for uniqueness
        :param email: email to validate
        :return: None
        :raises: ValidationError
    """
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exists")


def validate_email_for_other_users(email: str, user_id: int) -> None:
    """
    Validate email for uniqueness for other users
    :param email: email to validate
    :param user_id: user id
    :return: None
    :raises: ValidationError
    """
    if User.objects.filter(email=email).exclude(id=user_id).exists():
        raise ValidationError("Email already exists")
