from datetime import datetime, timedelta
import requests
import Movies_Library_API.config as config
from django.conf import settings
from .generic_requests import GenericRequests


class MovieRequests(GenericRequests):
    media_type = 'movie'

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

    # _URL = settings.API_URL
    #
    # def get_popular_movies(
    #     self, page: int = 1, language: str = "en-US", region: str = "US"
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "movie/popular",
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "page": page,
    #             "region": region,
    #         },
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_movie_details(
    #     self, movie_id: int, language: str = "en-US", region: str = "US"
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "movie/" + str(movie_id),
    #         params={"api_key": config.api_key, "language": language, "region": region},
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_upcoming_movies(
    #     self,
    #     page: int = 1,
    #     time_type_start_offset: str = "month",
    #     language: str = "en-US",
    #     region: str = "US",
    # ) -> dict | None:
    #     start_time = datetime.now()
    #
    #     if time_type_start_offset == "month":
    #         start_time = datetime.now() + timedelta(days=30)
    #     elif time_type_start_offset == "week":
    #         start_time = datetime.now() + timedelta(days=7)
    #
    #     end_time = start_time + timedelta(days=14)
    #
    #     response = requests.get(
    #         url=self._URL + "discover/movie",
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "region": region,
    #             "primary_release_date.gte": start_time.strftime("%Y-%m-%d"),
    #             "primary_release_date.lte": end_time.strftime("%Y-%m-%d"),
    #             "sort_by": "release_date.asc",
    #             "page": page,
    #         },
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_latest_movies(
    #     self,
    #     page: int = 1,
    #     language: str = "en-US",
    #     region: str = "US",
    # ) -> (
    #     dict | None
    # ):  # TODO: change latest definition. It should be the latest movie with is now playing
    #     response = requests.get(
    #         url=self._URL + "movie/latest",  # TODO: change to discover endpoint
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "region": region,
    #             "page": page,
    #         },
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_now_playing_movies(
    #     self, page: int = 1, language: str = "en-US", region: str = "US"
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "movie/now_playing",
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "page": page,
    #             "region": region,
    #         },
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_trending_movie_by_media_and_time(
    #     self,
    #         media_type: str,
    #         time_window: str,
    #         page: int = 1,
    #         language: str = "en-US",
    #         region: str = "US",
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "trending/" + media_type + "/" + time_window,
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "page": page,
    #             "region": region,
    #         },
    #     )
    #     return response.json()
    #
    # def get_movie_credits(
    #     self, movie_id: int, language: str = "en-US", region: str = "US"
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "movie/" + str(movie_id) + "/credits",
    #         params={"api_key": config.api_key, "language": language, "region": region},
    #     )
    #     if response.status_code == 200:
    #         return response.json()["cast"]
    #     return None
    #
    # def get_movie_recommendations(
    #     self, movie_id: int, page: int = 1, language: str = "en-US", region: str = "US"
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "movie/" + str(movie_id) + "/recommendations",
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "page": page,
    #             "region": region,
    #         },
    #     )
    #
    #     if response.status_code == 200:
    #         return response.json()
    #
    #     return None
    #
    # def get_similar_movies(
    #     self, movie_id: int, page: int = 1, language: str = "en-US", region: str = "US"
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "movie/" + str(movie_id) + "/similar",
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "page": page,
    #             "region": region,
    #         },
    #     )
    #
    #     if response.status_code == 200:
    #         return response.json()
    #
    #     return None
    #
    # def get_movie_provider(
    #     self, movie_id: int, country_code: str = "US", language: str = "en-US"
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "movie/" + str(movie_id) + "/watch/providers",
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "region": country_code,
    #         },
    #     )
    #
    #     if response.status_code == 200:
    #         return response.json()["results"][country_code.upper()]
    #
    #     return None
    #
    # def search_movie(
    #     self, query: str, page: str = 1, language: str = "en-US", region: str = "US"
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "search/movie",
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "query": query,
    #             "region": region,
    #             "page": page,
    #         },
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_genres(self, language: str = "en-US") -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "genre/movie/list",
    #         params={"api_key": config.api_key, "language": language},
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_movies_by_genre(
    #     self, genre_ids: str, page: int = 1, language: str = "en-US"
    # ) -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "discover/movie",
    #         params={
    #             "api_key": config.api_key,
    #             "language": language,
    #             "page": page,
    #             "with_genres": genre_ids,
    #         },
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
    #
    # def get_movie_videos(self, movie_id: int, language: str = "en-US") -> dict | None:
    #     response = requests.get(
    #         url=self._URL + "movie/" + str(movie_id) + "/videos",
    #         params={"api_key": config.api_key, "language": language},
    #     )
    #     if response.status_code == 200:
    #         return response.json()
    #     return None
