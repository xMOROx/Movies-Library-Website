from datetime import datetime, timedelta

import Movies_Library_API.config as config
import requests
from django.conf import settings


class GenericRequests:
    _URL = settings.API_URL
    media_type = ""

    def get_popular(
            self, page: int = 1, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/popular",
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

    def get_details(
            self, movie_id: int, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/" + str(movie_id),
            params={"api_key": config.api_key, "language": language, "region": region},
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_upcoming(
            self,
            page: int = 1,
            time_type_start_offset: str = "month",
            language: str = "en-US",
            region: str = "US",
    ) -> dict | None:
        start_time = datetime.now()

        if time_type_start_offset == "month":
            start_time = datetime.now() + timedelta(days=30)
        elif time_type_start_offset == "week":
            start_time = datetime.now() + timedelta(days=7)

        end_time = start_time + timedelta(days=14)

        response = requests.get(
            url=self._URL + f"discover/{self.media_type}",
            params={
                "api_key": config.api_key,
                "language": language,
                "region": region,
                "primary_release_date.gte": start_time.strftime("%Y-%m-%d"),
                "primary_release_date.lte": end_time.strftime("%Y-%m-%d"),
                "sort_by": "release_date.asc",
                "page": page,
            },
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_latest(
            self,
            page: int = 1,
            language: str = "en-US",
            region: str = "US",
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/latest",
            params={
                "api_key": config.api_key,
                "language": language,
                "region": region,
                "page": page,
            },
        )
        if response.status_code == 200:
            return response.json()
        return None

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

    def get_trending_by_time(
            self,
            time_window: str,
            page: int = 1,
            language: str = "en-US",
            region: str = "US",
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"trending/{self.media_type}/" + time_window,
            params={
                "api_key": config.api_key,
                "language": language,
                "page": page,
                "region": region,
            },
        )
        return response.json()

    def get_credits(
            self, content_id: int, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/{content_id}/credits",
            params={"api_key": config.api_key, "language": language, "region": region},
        )
        if response.status_code == 200:
            return response.json()["cast"]
        return None

    def get_recommendations(
            self,
            content_id: int,
            page: int = 1,
            language: str = "en-US",
            region: str = "US",
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/{content_id}/recommendations",
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

    def get_similar(
            self,
            content_id: int,
            page: int = 1,
            language: str = "en-US",
            region: str = "US",
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/{content_id}/similar",
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

    def get_provider(
            self, content_id: int, country_code: str = "US", language: str = "en-US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/{content_id}/watch/providers",
            params={
                "api_key": config.api_key,
                "language": language,
                "region": country_code,
            },
        )

        if response.status_code == 200:
            return response.json()["results"][country_code.upper()]

        return None

    def search(
            self, query: str, page: str = 1, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"search/{self.media_type}",
            params={
                "api_key": config.api_key,
                "language": language,
                "query": query,
                "region": region,
                "page": page,
            },
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_genres(self, language: str = "en-US") -> dict | None:
        response = requests.get(
            url=self._URL + f"genre/{self.media_type}/list",
            params={"api_key": config.api_key, "language": language},
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_content_by_genre(
            self, genre_ids: str, page: int = 1, language: str = "en-US"
    ) -> dict | None:
        response = requests.get(
            url=self._URL + f"discover/{self.media_type}",
            params={
                "api_key": config.api_key,
                "language": language,
                "page": page,
                "with_genres": genre_ids,
            },
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_videos(self, content_id: int, language: str = "en-US") -> dict | None:
        response = requests.get(
            url=self._URL + f"{self.media_type}/{content_id}/videos",
            params={"api_key": config.api_key, "language": language},
        )
        if response.status_code == 200:
            return response.json()
        return None
