import Movies_Library_API.config as config
import requests
from django.conf import settings


class ActorsRequest:
    """
    Class for actors requests from The Movie Database API
    """

    _URL = settings.API_URL

    def get_actors(self, language: str = "en-US", page: int = 1) -> dict | None:
        """
        Get a list of popular actors on TMDb. This list updates daily.
        :param language: language of the response. Default is "en-US"
        :param page: page of the response. Default is 1
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + "person/popular",
            params={"api_key": config.api_key, "language": language, "page": page},
        )

        if response.status_code == 200:
            return response.json()

        return None

    def get_actor_details(self, actor_id: int, language: str = "en-US") -> dict | None:
        """
        Get the primary person details by id.
        :param actor_id: actor id
        :param language: language of the response. Default is "en-US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

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
        """
        Get the external ids for a person. We currently support the following external sources.
        :param actor_id: actor id
        :param language: language of the response. Default is "en-US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + "person/" + str(actor_id) + "/external_ids",
            params={"api_key": config.api_key, "language": language},
        )

        if response.status_code == 200:
            return response.json()

        return None

    def get_person_cast(self, actor_id: int, language: str = "en-US") -> dict | None:
        """
        Get the movie and TV credits together in a single response.
        :param actor_id: actor id
        :param language: language of the response. Default is "en-US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

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
        # TODO: add time_window validation and change it to enum
        """
        Get the daily or weekly trending actors. The daily trending list tracks items over the period of a day while
        items have a 24 hour half life. The weekly list tracks items over a 7-day period, with a 7 day half life.
        :param language: language of the response. Default is "en-US"
        :param time_window: time window of the response. Available value is "day" or "week". Default is "week"
        :param page: page of the response. Default is 1
        :return: dict | None if response status code is not 200 (something went wrong)
        """

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
