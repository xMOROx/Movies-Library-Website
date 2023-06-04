from Movies_Library_API.requests.actors_requests import ActorsRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def get_actor_details(_, actor_id: int) -> JsonResponse:
    """
    Get actor details
    :param _: request - not used
    :param actor_id: actor id
    :return: JsonResponse with actor details and status code(200) or error message (status 404)
    Allowing any user to access this endpoint
    """
    actor_request = ActorsRequest()
    actor_details = actor_request.get_actor_details(actor_id)

    if actor_details is None:
        return JsonResponse(
            {"message": "Actor not found."}, status=status.HTTP_404_NOT_FOUND
        )

    return JsonResponse(actor_details, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_actor_external_data(_, actor_id: int) -> JsonResponse:
    """
    Get actor external data
    :param _: request - not used
    :param actor_id: actor id
    :return: JsonResponse with external data and status code(200) or error message (status 404)
    Allowing any user to access this endpoint
    """

    actor_request = ActorsRequest()
    actor_external_data = actor_request.get_actor_external_data(actor_id)

    if actor_external_data is None:
        return JsonResponse(
            {"message": "Actor not found."}, status=status.HTTP_404_NOT_FOUND
        )

    return JsonResponse(actor_external_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_actor_cast(_, actor_id: int) -> JsonResponse:
    """
    Get actor cast
    :param _: request - not used
    :param actor_id: actor id
    :return: JsonResponse with list of movies and status code(200) or error message (status 404)
    Allowing any user to access this endpoint
    """

    actor_request = ActorsRequest()
    actor_cast = actor_request.get_person_cast(actor_id)

    if actor_cast is None:
        return JsonResponse(
            {"message": "Actor not found."}, status=status.HTTP_404_NOT_FOUND
        )

    return JsonResponse(actor_cast, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_trending_actors(request) -> JsonResponse:
    """
    Get trending actors
    :param request: request
    :return: JsonResponse with list of trending actors and status code(200) or error message (status 404)
    Allowing any user to access this endpoint
    """

    actor_request = ActorsRequest()
    time_window = request.GET.get("time_window", "week")
    language = request.GET.get("language", "en-US")
    page = request.GET.get("page", 1)

    trending_actors = actor_request.get_trending_actors(
        language=language, time_window=time_window, page=page
    )

    if trending_actors is None:
        return JsonResponse(
            {"message": "Trending actors not found."}, status=status.HTTP_404_NOT_FOUND
        )

    return JsonResponse(trending_actors, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_actors(request) -> JsonResponse:
    """
    Get list of actors
    :param request: request
    :return: JsonResponse with list of actors and status code(200) or error message (status 404)
    Allowing any user to access this endpoint
    """

    actor_request = ActorsRequest()
    language = request.GET.get("language", "en-US")
    page = request.GET.get("page", 1)

    actors = actor_request.get_actors(language=language, page=page)

    if actors is None:
        return JsonResponse(
            {"message": "Actors not found."}, status=status.HTTP_404_NOT_FOUND
        )

    return JsonResponse(actors, status=status.HTTP_200_OK)
