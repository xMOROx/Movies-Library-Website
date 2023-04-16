from rest_framework import views, response, exceptions, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
)
from .serializers import UserSerializer
from .models import User


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        id = serializer.data.get("id")

        response_data = {"User id": id, "message": "User created successfully"}

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


class UserListView(views.APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request):
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)

        return response.Response(serializer.data)


class AdminUserUpdateView(views.APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def patch(self, request, user_id, format=None):
        if "is_banned" in request.data:
            return response.Response(
                {
                    "message": "You can't change is_banned field from here. Use /api/v1/auth/users/{id}/ban/ endpoint"
                },
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.NotFound("User does not exist")

        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=HTTP_200_OK)
        return response.Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.NotFound("User does not exist")

        user.delete()

        return response.Response(status=HTTP_204_NO_CONTENT)


class BanUserView(views.APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def patch(self, request, user_id):
        if "is_banned" not in request.data:
            return response.Response(
                {"message": "You should provide is_banned field"},
                status=HTTP_400_BAD_REQUEST,
            )

        if not isinstance(request.data["is_banned"], bool):
            return response.Response(
                {"message": "is_banned field should be boolean"},
                status=HTTP_400_BAD_REQUEST,
            )

        if len(request.data) > 1:
            return response.Response(
                {
                    "message": "You can't change other fields from here. Use /api/v1/auth/users/{id}/ endpoint"
                },
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.NotFound("User does not exist")

        if request.data["is_banned"] == user.is_banned:
            return response.Response(
                {
                    "message": "User is already banned"
                    if request.data["is_banned"]
                    else "User is already unbanned"
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
