from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exists")
