from django.conf import settings
import requests
import Movies_Library_API.config as config


class ActorsRequest:
    _URL = settings.API_URL

    def getActorDetails(self, actor_id: int, language: str = "en-US") -> dict | None:
        response = requests.get(
            url=self._URL + "person/" + str(actor_id),
            params={"api_key": config.api_key, "language": language},
        )
        if response.status_code == 200:
            return response.json()

        return None

    def getActorExternalData(
        self, actor_id: int, language: str = "en-US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + "person/" + str(actor_id) + "/external_ids",
            params={"api_key": config.api_key, "language": language},
        )
        if response.status_code == 200:
            return response.json()

        return None

    def getPersonCast(self, actor_id: int, language: str = "en-US") -> dict | None:
        response = requests.get(
            url=self._URL + "person/" + str(actor_id) + "/movie_credits",
            params={"api_key": config.api_key, "language": language},
        )
        if response.status_code == 200:
            return response.json()

        return None
