from rest_framework import views, response, exceptions, permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_200_OK,

)
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsOwner
from .serializers import UserSerializer, ChangePasswordSerializer
from .models import User

from rest_framework.exceptions import ValidationError


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
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.NotFound("User does not exist")

        serializer = UserSerializer(user)

        return response.Response(serializer.data)

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.NotFound("User does not exist")

        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.NotFound("User does not exist")

        user.delete()

        return response.Response(status=HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    JSON FORMAT:
    For example:
    {
      "user": {
        "id": 1
      },
          "old_password":"old_password
          "new_password1":"new_password",
          "new_password2":"new_password"
      }
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    authentication_classes = [JWTAuthentication]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return response.Response(
                {"message": "Invalid data", "status": HTTP_400_BAD_REQUEST, "errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        return response.Response(
            status=HTTP_204_NO_CONTENT,
        )