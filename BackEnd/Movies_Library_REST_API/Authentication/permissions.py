from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions

User = get_user_model()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = view.kwargs.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        return user == request.user
