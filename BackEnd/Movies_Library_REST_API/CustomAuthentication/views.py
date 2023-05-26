from CustomAuthentication.models import User
from CustomAuthentication.permissions import IsOwner
from CustomAuthentication.serializers import UserSerializer, ChangePasswordSerializer, UserUpdateSerializer
from CustomAuthentication.validators import validate_email_for_other_users
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import views, response, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND,

)
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return response.Response(
                {"message": "Email already exists", "status": HTTP_409_CONFLICT},
                status=HTTP_409_CONFLICT,
            )

        serializer.save()

        id = serializer.data.get("id")

        response_data = {
            "User id": id,
            "message": "User created successfully",
            "status": HTTP_201_CREATED,
        }

        return response.Response(response_data, status=HTTP_201_CREATED)


class UserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    lookup_field = "user_id"

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return response.Response(
                {"message": "User does not exist", "status": HTTP_404_NOT_FOUND, "id": user_id},
                status=HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(user)

        return response.Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return response.Response(
                {"message": "User does not exist", "status": HTTP_404_NOT_FOUND, "id": user_id},
                status=HTTP_404_NOT_FOUND,
            )

        serializer = UserUpdateSerializer(user, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return response.Response(
                {"message": "Error occur", "status": HTTP_400_BAD_REQUEST},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            validate_email_for_other_users(serializer.validated_data["email"], user_id)
        except DjangoValidationError:
            return response.Response(
                {"message": "Email already exists", "status": HTTP_409_CONFLICT},
                status=HTTP_409_CONFLICT,
            )

        serializer.save()

        return response.Response(serializer.data, status=HTTP_204_NO_CONTENT)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return response.Response(
                {"message": "User does not exist", "status": HTTP_400_BAD_REQUEST, "id": user_id},
                status=HTTP_400_BAD_REQUEST,
            )

        user.delete()

        return response.Response(status=HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    JSON FORMAT:
    For example:
    {
          "password":"old_password",
          "new_password":"new_password",
          "confirm_password":"new_password"
    }
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    authentication_classes = [JWTAuthentication]
    lookup_field = "user_id"

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return response.Response(
                {"message": e.detail["message"][0], "status": HTTP_409_CONFLICT, "errors": serializer.errors},
                status=HTTP_409_CONFLICT,
            )

        serializer.save()

        return response.Response(
            status=HTTP_204_NO_CONTENT,
        )
