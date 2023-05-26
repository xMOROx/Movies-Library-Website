from CustomAuthentication.models import User
from CustomAuthentication.serializers import AdminUserSerializer, AdminChangePasswordSerializer
from rest_framework import views, response, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.status import (
    HTTP_409_CONFLICT,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_200_OK,

)
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserListView(views.APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return response.Response(serializer.data, status=HTTP_200_OK)


class UpdateUserView(UpdateAPIView):
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


class ChangePasswordForUserView(UpdateAPIView):
    """
    An endpoint for changing password.
    JSON FORMAT:
    For example:
    {
      "new_password":"new_password"
    }
    """
    queryset = User.objects.all()
    serializer_class = AdminChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return response.Response(
                {"message": "Invalid data", "status": HTTP_400_BAD_REQUEST, "errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return response.Response(
            status=HTTP_204_NO_CONTENT,
        )
