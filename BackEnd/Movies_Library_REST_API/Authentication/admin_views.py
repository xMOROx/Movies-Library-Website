from rest_framework import views, response, exceptions, permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_200_OK,

)
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import AdminUserSerializer
from .models import User

from rest_framework.exceptions import ValidationError


class UserListView(views.APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return response.Response(serializer.data, status=HTTP_200_OK)


class UpdateUser(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return response.Response(
                {"message": "Email already exists", "status": HTTP_409_CONFLICT},
                status=HTTP_409_CONFLICT,
            )

        serializer.save()

        return response.Response(
            {"message": "User updated successfully", "status": HTTP_204_NO_CONTENT},
            status=HTTP_204_NO_CONTENT)
