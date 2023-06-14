from CustomAuthentication.models import User
from CustomAuthentication.serializers import AdminUserSerializer, AdminChangePasswordSerializer
from rest_framework import views, response, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.status import (
    HTTP_409_CONFLICT,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND,

)
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserListView(views.APIView):
    """
    An endpoint for getting all users by admin.
    Order by id descending.
    """
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self) -> response.Response:
        users = User.objects.all().order_by("-id")
        serializer = self.serializer_class(users, many=True)
        return response.Response(serializer.data, status=HTTP_200_OK)


class UpdateUserView(UpdateAPIView):
    """
    An endpoint for updating user data by admin.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    lookup_field = "id"

    def update(self, request, *args, **kwargs) -> response.Response:
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
    An endpoint for changing password for user by admin.
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

    def update(self, request, *args, **kwargs) -> response.Response:
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


class BanUserView(views.APIView):
    """
    An endpoint for banning user by admin.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def patch(self, request, user_id):
        if "is_banned" not in request.data:
            return response.Response(
                {"message": "You should provide is_banned field."},
                status=HTTP_400_BAD_REQUEST,
            )

        if len(request.data) > 1:
            return response.Response(
                {
                    "message": "You can't change other fields from here. Use /api/v1/auth/users/{id}/ endpoint."
                },
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return response.Response(
                {
                    "message": "User does not exist.",
                    "status": HTTP_404_NOT_FOUND,
                    "id": user_id,
                },
                status=HTTP_404_NOT_FOUND,
            )

        is_banned = (
            False
            if request.data["is_banned"] == "False"
            else bool(request.data["is_banned"])
        )

        if is_banned == user.is_banned:
            return response.Response(
                {
                    "message": "User is already banned."
                    if is_banned
                    else "User is already unbanned."
                },
                status=HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            msg = (
                f"User with id:{user_id} banned successfully "
                if request.data["is_banned"]
                else f"User with id:{user_id} unbanned successfully"
            )
            # msg += "and email has been sent to user" #TODO: add sending email and reason for ban
            return response.Response({"message": msg}, status=HTTP_200_OK)

        return response.Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
