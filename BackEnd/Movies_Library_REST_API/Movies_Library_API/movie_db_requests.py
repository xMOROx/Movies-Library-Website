from datetime import datetime, timedelta
import requests
import Movies_Library_API.config as config
from django.conf import settings


class MovieRequests:
    _URL = settings.API_URL

    def get_popular_movies(self, page: int = 1) -> dict | None:
        if page is None:
            page = 1

        response = requests.get(
            url=self._URL + "movie/popular",
            params={"api_key": config.api_key, "language": "en-US", "page": page},
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_movie_details(self, movie_id: int) -> dict | None:
        response = requests.get(
            url=self._URL + "movie/" + str(movie_id),
            params={"api_key": config.api_key, "language": "en-US"},
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_upcoming_movies(
        self, page: int = 1, time_type_start_offset: str = "month"
    ) -> dict | None:
        start_time = datetime.now()
        if page is None:
            page = 1
        if time_type_start_offset is None:
            time_type_start_offset = "month"

        if time_type_start_offset == "month":
            start_time = datetime.now() + timedelta(days=30)
        elif time_type_start_offset == "week":
            start_time = datetime.now() + timedelta(days=7)

        end_time = start_time + timedelta(days=14)

        response = requests.get(
            url=self._URL + "discover/movie",
            params={
                "api_key": config.api_key,
                "language": "en-US",
                "region": "US",
                "primary_release_date.gte": start_time.strftime("%Y-%m-%d"),
                "primary_release_date.lte": end_time.strftime("%Y-%m-%d"),
                "sort_by": "release_date.asc",
                "page": page,
            },
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_latest_movies(
        self,
    ) -> (
        dict | None
    ):  # TODO: change latest definition. It should be the latest movie with is now playing
        response = requests.get(
            url=self._URL + "movie/latest",  # TODO: change to discover endpoint
            params={"api_key": config.api_key, "language": "en-US"},
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_now_playing_movies(self, page: int = 1) -> dict | None:
        response = requests.get(
            url=self._URL + "movie/now_playing",
            params={"api_key": config.api_key, "language": "en-US", "page": page},
        )
        if response.status_code == 200:
            return response.json()
        return None

    def get_treding_movie_by_media_and_time(
        self, media_type: str, time_window: str, page: int = 1
    ) -> dict | None:
        if page is None:
            page = 1
        response = requests.get(
            url=self._URL + "trending/" + media_type + "/" + time_window,
            params={"api_key": config.api_key, "language": "en-US", "page": page},
        )
        return response.json()

    def get_movie_credits(self, movie_id: int) -> dict | None:
        response = requests.get(
            url=self._URL + "movie/" + str(movie_id) + "/credits",
            params={"api_key": config.api_key, "language": "en-US"},
        )
        if response.status_code == 200:
            return response.json()["cast"]
        return None

    def get_movie_recommendations(self, movie_id: int, page: int = 1) -> dict | None:
        if page is None:
            page = 1

        response = requests.get(
            url=self._URL + "movie/" + str(movie_id) + "/recommendations",
            params={"api_key": config.api_key, "language": "en-US", "page": page},
        )

        if response.status_code == 200:
            return response.json()

        return None

    def get_similar_movies(self, movie_id: int, page: int = 1) -> dict | None:
        if page is None:
            page = 1

        response = requests.get(
            url=self._URL + "movie/" + str(movie_id) + "/similar",
            params={"api_key": config.api_key, "language": "en-US", "page": page},
        )

        if response.status_code == 200:
            return response.json()

        return None

    def get_movie_provider(
        self, movie_id: int, country_code: str = "US"
    ) -> dict | None:
        if country_code is None:
            country_code = "US"

        response = requests.get(
            url=self._URL + "movie/" + str(movie_id) + "/watch/providers",
            params={"api_key": config.api_key, "language": "en-US"},
        )

        if response.status_code == 200:
            return response.json()["results"][country_code.upper()]

        return None

    def get_movies_by_query(self, query: str) -> dict | None:
        response = requests.get(
            url=self._URL + "search/movie",
            params={"api_key": config.api_key, "language": "en-US", "query": query},
        )
        if response.status_code == 200:
            return response.json()
        return None
