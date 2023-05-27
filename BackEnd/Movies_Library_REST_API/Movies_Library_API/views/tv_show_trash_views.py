from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models.movie_lib_models import TVShow, TVShowTrash
from Movies_Library_API.serializers import TVShowTrashSerializer
from CustomAuthentication.models import User
from CustomAuthentication.permissions import IsOwner

from ..requests.tv_shows_requests import TVShowsRequests
from rest_framework.serializers import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def crud_for_tv_show_inside_trash(request, user_id, tv_show_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            _ = TVShow.objects.get(pk=tv_show_id)
        except TVShow.DoesNotExist:
            return JsonResponse(
                {"message": "This tv show does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            data = TVShowTrash.objects.get(user=user_id, tv_show=tv_show_id)
        except TVShowTrash.DoesNotExist:
            return JsonResponse(
                {"message": "This tv show is not in trash"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TVShowTrashSerializer(data)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        tv_show_requests = TVShowsRequests()

        try:
            tv_show = TVShow.objects.get(pk=tv_show_id)
        except TVShow.DoesNotExist:
            tv_show_api = tv_show_requests.get_details(tv_show_id)
            if tv_show_api is None:
                return JsonResponse(
                    {"message": "This tv show does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                tv_show = TVShow.objects.create(
                    id=tv_show_api["id"],
                    title=tv_show_api["name"],
                    poster_url=tv_show_api["poster_path"],
                )
            except (DRFValidationError, DjangoValidationError) as e:
                return JsonResponse(
                    {"message": "The tv show could not be added"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            _ = TVShowTrash.objects.get(user=user_id, tv_show=tv_show_id)
            return JsonResponse(
                {"message": "Tv show already in trash"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except TVShowTrash.DoesNotExist:
            tv_show_trash = TVShowTrash.objects.create(
                user=user,
                tv_show=tv_show
            )
            tv_show_trash.save()

            serializer = TVShowTrashSerializer(tv_show_trash)

            return JsonResponse(
                serializer.data, status=status.HTTP_201_CREATED, safe=False
            )
    elif request.method == "DELETE":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            _ = TVShow.objects.get(pk=tv_show_id)
        except TVShow.DoesNotExist:
            return JsonResponse(
                {"message": "This tv show does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        tv_show_trash = get_object_or_404(TVShowTrash, user=user_id, tv_show=tv_show_id)
        tv_show_trash.delete()
        return JsonResponse(
            None, status=status.HTTP_204_NO_CONTENT, safe=False
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def get_all_tv_shows(request, user_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        show_all = "true" == request.GET.get("all", 1)
        data = get_list_or_404(TVShowTrash.objects.order_by("-tv_show__title"), user=user_id)
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(data, request)
        if page is not None and not show_all:
            serializer = TVShowTrashSerializer(page, many=True)
            return pagination.get_paginated_response(serializer.data)

        serializer = TVShowTrashSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)

