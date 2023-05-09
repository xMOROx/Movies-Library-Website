from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_actor_details(_, actor_id):
    from Movies_Library_API.requests.actors_requests import ActorsRequest

    actor_request = ActorsRequest()
    actor_details = actor_request.getActorDetails(actor_id)
    if actor_details is None:
        return JsonResponse(
            {"message": "Actor not found"}, status=status.HTTP_404_NOT_FOUND
        )
    return JsonResponse(actor_details, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_actor_external_data(_, actor_id):
    from Movies_Library_API.requests.actors_requests import ActorsRequest

    actor_request = ActorsRequest()
    actor_external_data = actor_request.getActorExternalData(actor_id)
    if actor_external_data is None:
        return JsonResponse(
            {"message": "Actor not found"}, status=status.HTTP_404_NOT_FOUND
        )
    return JsonResponse(actor_external_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_actor_cast(_, actor_id):
    from Movies_Library_API.requests.actors_requests import ActorsRequest

    actor_request = ActorsRequest()
    actor_cast = actor_request.getPersonCast(actor_id)
    if actor_cast is None:
        return JsonResponse(
            {"message": "Actor not found"}, status=status.HTTP_404_NOT_FOUND
        )
    return JsonResponse(actor_cast, status=status.HTTP_200_OK)
