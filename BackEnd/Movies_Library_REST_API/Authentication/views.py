from rest_framework import views, response, exceptions, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
)
from .serializers import UserSerializer
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
