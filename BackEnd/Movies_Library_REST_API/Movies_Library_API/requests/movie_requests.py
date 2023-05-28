from datetime import datetime, timedelta
import requests
import Movies_Library_API.config as config
from django.conf import settings
from .generic_requests import GenericRequests


class MovieRequests(GenericRequests):
    media_type = "movie"

    def get_now_playing(
        self, page: int = 1, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/now_playing",
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
