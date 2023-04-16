import datetime
from rest_framework import serializers
from .models import User
from .validators import validate_email


class UserSerializer(serializers.ModelSerializer):
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
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user

    def update(self, instance, validated_data):
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


class AdminUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + (
            "is_staff",
            "is_superuser",
            "is_banned",
            "is_active",
        )

    def update(self, instance, validated_data):
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
