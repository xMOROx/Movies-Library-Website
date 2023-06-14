from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True


        jwt_object = JWTAuthentication()
        header = jwt_object.get_header(request)
        raw_token = jwt_object.get_raw_token(header)
        validated_token = jwt_object.get_validated_token(raw_token)

        user = jwt_object.get_user(validated_token)

        return user.id == int(view.kwargs.get("user_id"))
