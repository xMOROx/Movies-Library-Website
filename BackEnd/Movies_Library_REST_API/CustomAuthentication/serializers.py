from CustomAuthentication.models import User
from CustomAuthentication.utils.validators import validate_email
from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user
    """
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True, validators=[validate_email])

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user

    def update(self, instance, validated_data) -> User:
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            del validated_data["password"]

        if "email" in validated_data:
            instance.email = validated_data["email"]
            del validated_data["email"]

        if "first_name" in validated_data:
            instance.first_name = validated_data["first_name"]
            del validated_data["first_name"]

        if "last_name" in validated_data:
            instance.last_name = validated_data["last_name"]
            del validated_data["last_name"]

        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )

    def update(self, instance, validated_data) -> User:
        if "email" in validated_data:
            instance.email = validated_data["email"]
            del validated_data["email"]

        if "first_name" in validated_data:
            instance.first_name = validated_data["first_name"]
            del validated_data["first_name"]

        if "last_name" in validated_data:
            instance.last_name = validated_data["last_name"]
            del validated_data["last_name"]

        instance.save()
        return instance


class AdminUserSerializer(UserSerializer):
    """
    Serializer for admin user
    """

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + (
            "is_staff",
            "is_superuser",
            "is_banned",
            "is_active",
        )

    def update(self, instance, validated_data) -> User:
        instance = super().update(instance, validated_data)
        if "is_staff" in validated_data:
            instance.is_staff = validated_data["is_staff"]
            del validated_data["is_staff"]

        if "is_superuser" in validated_data:
            instance.is_superuser = validated_data["is_superuser"]
            del validated_data["is_superuser"]

        if "is_banned" in validated_data:
            instance.is_banned = validated_data["is_banned"]
            del validated_data["is_banned"]

        if "is_active" in validated_data:
            instance.is_active = validated_data["is_active"]
            del validated_data["is_active"]

        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> str:
        token = super().get_token(user)
        return token


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint for normal users.
    """
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value: str) -> str:
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {'message': 'Your old password was entered incorrectly. Please enter it again.'}
            )
        return value

    def validate(self, data: dict) -> dict:
        self.validate_old_password(data['password'])
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'message': "The two password fields didn't match."})
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data

    def save(self, **kwargs) -> User:
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class AdminChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint for admin users.
    """
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data: dict) -> dict:
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data

    def save(self, **kwargs) -> User:
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
