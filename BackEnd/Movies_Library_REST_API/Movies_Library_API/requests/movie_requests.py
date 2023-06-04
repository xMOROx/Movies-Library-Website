import Movies_Library_API.config as config
import requests

from .generic_requests import GenericRequests


class MovieRequests(GenericRequests):
    _media_type = "movie"

    def get_now_playing(
            self, page: int = 1, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        """
        Get a list of now playing movies in theatres.
        :param page: Specify which page to query. Default is 1.
        :param language: Specify a language to query translatable fields with. Default is "en-US".
        :param region: Specify a ISO 3166-1 code to filter release dates. Default is "US".
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"{self._media_type}/now_playing",
            params={
                "api_key": config.api_key,
                "language": language,
                "page": page,
                "region": region.upper(),
            },
        )

        if response.status_code == 200:
            return response.json()
        return None
