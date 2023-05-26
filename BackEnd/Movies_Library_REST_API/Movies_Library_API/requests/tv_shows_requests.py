from datetime import datetime, timedelta
import requests
import Movies_Library_API.config as config
from django.conf import settings
from .generic_requests import GenericRequests


class TVShowsRequests(GenericRequests):
    _URL = settings.API_URL
    media_type = 'TV'

    def get_airing_today(
            self, page: int = 1, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/airing_today",
            params={
                "api_key": config.api_key,
                "language": language,
                "page": page,
                "region": region,
            },
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_airing_this_week(
            self, page: int = 1, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/on_the_air",
            params={
                "api_key": config.api_key,
                "language": language,
                "page": page,
                "region": region,
            },
        )
        if response.status_code == 200:
            return response.json()
        return None
