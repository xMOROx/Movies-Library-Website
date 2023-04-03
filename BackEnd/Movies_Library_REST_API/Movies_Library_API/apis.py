from rest_framework import views, response, exceptions, permissions

from .serializers import UserSerializer
from . import services


class RegisterAPI(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        serializer.instance = services.create_user(user_data_class=data)

        return response.Response(data=serializer.data, status=201)


class LoginAPI(views.APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = services.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid credentials")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid credentials")

        token = services.create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserAPI(views.APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return response.Response(data=serializer.data)
