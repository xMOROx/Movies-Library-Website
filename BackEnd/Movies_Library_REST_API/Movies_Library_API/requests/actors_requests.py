from django.conf import settings
import requests
import Movies_Library_API.config as config


class ActorsRequest:
    _URL = settings.API_URL

    def get_actors(self, language: str = "en-US", page: int = 1) -> dict | None:
        response = requests.get(
            url=self._URL + "person/popular",
            params={"api_key": config.api_key, "language": language, "page": page},
        )
        if response.status_code == 200:
            return response.json()

        return None

    def get_actor_details(self, actor_id: int, language: str = "en-US") -> dict | None:
        response = requests.get(
            url=self._URL + "person/" + str(actor_id),
            params={"api_key": config.api_key, "language": language},
        )
        if response.status_code == 200:
            return response.json()

        return None

    def get_actor_external_data(
        self, actor_id: int, language: str = "en-US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + "person/" + str(actor_id) + "/external_ids",
            params={"api_key": config.api_key, "language": language},
        )
        if response.status_code == 200:
            return response.json()

        return None

    def get_person_cast(self, actor_id: int, language: str = "en-US") -> dict | None:
        response = requests.get(
            url=self._URL + "person/" + str(actor_id) + "/movie_credits",
            params={"api_key": config.api_key, "language": language},
        )
        if response.status_code == 200:
            return response.json()

        return None

    def get_trending_actors(
        self, language: str = "en-US", time_window: str = "week", page: int = 1
    ) -> dict | None:
        response = requests.get(
            url=self._URL + "trending/person/week",
            params={
                "api_key": config.api_key,
                "language": language,
                "time_window": time_window,
                "page": page,
            },
        )
        if response.status_code == 200:
            return response.json()

        return None
