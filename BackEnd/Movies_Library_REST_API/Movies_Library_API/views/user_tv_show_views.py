from CustomAuthentication.models import User
from CustomAuthentication.permissions import IsOwner
from Movies_Library_API.serializers import TVShow_UserSerializer
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    ObjectDoesNotExist,
    MultipleObjectsReturned,
)
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication

from Movies_Library_API.models.movie_lib_models import TVShow, TVShow_User
from Movies_Library_API.recommendations_algorithm import (
    collaborative_filtering_recommendation,
)
from Movies_Library_API.requests.tv_shows_requests import TVShowsRequests


@api_view(["PUT"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def add_tv_show_to_user(request, user_id, tv_show_id):
    if request.method == "PUT":
        tv_show_user = TVShow_User.objects.filter(
            user=user_id, tv_show=tv_show_id
        ).first()

        try:
            tv_show_user_serializer = TVShow_UserSerializer(data=request.data)
            tv_show_user_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return JsonResponse(
                {"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
            )

        if tv_show_user is not None:
            try:
                if "rating" in tv_show_user_serializer.validated_data:
                    tv_show_user.rating = tv_show_user_serializer.validated_data[
                        "rating"
                    ]

                if "is_favorite" in tv_show_user_serializer.validated_data:
                    tv_show_user.is_favorite = tv_show_user_serializer.validated_data[
                        "is_favorite"
                    ]

                if "status" in tv_show_user_serializer.validated_data:
                    tv_show_user.status = tv_show_user_serializer.validated_data[
                        "status"
                    ]

                if tv_show_user.status == "Not watched":
                    tv_show_user.delete()
                else:
                    tv_show_user.save()

                return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)
            except (DRFValidationError, DjangoValidationError) as e:
                return JsonResponse(
                    {"message": "The tv show could not be updated"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        tv_show_requests = TVShowsRequests()

        try:
            tv_show = TVShow.objects.get(pk=tv_show_id)
        except TVShow.DoesNotExist:
            tv_show_api = tv_show_requests.get_details(tv_show_id)

            if tv_show_api is None:
                return JsonResponse(
                    {
                        "message": f"The tv show with given id {tv_show_id} does not exist"
                    },
                    status=status.HTTP_404_NOT_FOUND,
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

        if "rating" not in tv_show_user_serializer.validated_data:
            tv_show_user_serializer.validated_data["rating"] = 0

        if "is_favorite" not in tv_show_user_serializer.validated_data:
            tv_show_user_serializer.validated_data["is_favorite"] = False

        if "status" not in tv_show_user_serializer.validated_data:
            tv_show_user_serializer.validated_data["status"] = "Not watched"

        tv_show_user = TVShow_User.objects.create(
            user=user,
            tv_show=tv_show,
            rating=tv_show_user_serializer.validated_data["rating"],
            is_favorite=tv_show_user_serializer.validated_data["is_favorite"],
            status=tv_show_user_serializer.validated_data["status"],
        )

        tv_show_user.save()

        return JsonResponse(
            tv_show_user_serializer.data, status=status.HTTP_201_CREATED, safe=False
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def list_of_details_for_tv_show_per_user(request, user_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        show_all = "true" == request.GET.get("all", 1)
        data = (
            TVShow_User.objects.select_related("tv_show")
            .filter(user_id=user_id)
            .order_by("-tv_show__title")
        )
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(data, request)
        if page is not None and not show_all:
            serializer = TVShow_UserSerializer(page, many=True)
            return pagination.get_paginated_response(serializer.data)

        serializer = TVShow_UserSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated & IsOwner])
@authentication_classes([JWTAuthentication])
def details_of_tv_show_for_user(request, user_id, tv_show_id):
    if request.method == "GET":
        try:
            _ = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            data = TVShow.users.through.objects.get(
                user_id=user_id, tv_show_id=tv_show_id
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"message": "The tv show does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except MultipleObjectsReturned:
            return JsonResponse(
                {"message": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer_tv_show_user = TVShow_UserSerializer(data)
        return JsonResponse(
            serializer_tv_show_user.data, safe=False, status=status.HTTP_200_OK
        )


# @api_view(["GET"])
# @permission_classes([IsAuthenticated & IsOwner])
# @authentication_classes([JWTAuthentication])
# def recommendations(request, user_id):
#     if request.method == "GET":
#         try:
#             _ = User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return JsonResponse(
#                 {"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND
#             )
#
#         tv_shows = collaborative_filtering_recommendation(user_id)
#         tv_shows_serialized = TVShow_UserSerializer(tv_shows, many=True)
#         data = {"tv_shows": tv_shows_serialized.data}
#         return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
