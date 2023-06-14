from datetime import datetime, timedelta

import Movies_Library_API.config as config
import requests
from django.conf import settings


class GenericRequests:
    """
    Generic requests class for all requests from TMDB API.
    """

    _URL = settings.API_URL
    _media_type = ""

    def get_popular(
        self, page: int = 1, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        """
        Get popular by '_media_type' from TMDB API.
        :param page: page number. Default is 1
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"{self._media_type}/popular",
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

    def get_details(
        self, movie_id: int, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        """
        Get details for a '_media_type' from TMDB API.
        :param movie_id: movie id
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """
        response = requests.get(
            url=self._URL + f"{self._media_type}/" + str(movie_id),
            params={
                "api_key": config.api_key,
                "language": language,
                "region": region.upper(),
            },
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
        """
        Get a list of upcoming '_media_type' in theatres or TV depends on '_media_type'.
        :param page: page number. Default is 1
        :param time_type_start_offset: time type start offset. Default is "month" TODO: change to enum
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
        :return: dict | None if response status code is not 200 (something went wrong)

        """

        start_time = datetime.now()

        if time_type_start_offset == "month":
            start_time = datetime.now() + timedelta(days=30)
        elif time_type_start_offset == "week":
            start_time = datetime.now() + timedelta(days=7)

        end_time = start_time + timedelta(days=14)

        response = requests.get(
            url=self._URL + f"discover/{self._media_type}",
            params={
                "api_key": config.api_key,
                "language": language,
                "region": region.upper(),
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
        """
        Get the most newly created '_media_type' entry.
        :param page: page number. Default is 1
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"{self._media_type}/latest",
            params={
                "api_key": config.api_key,
                "language": language,
                "region": region.upper(),
                "page": page,
            },
        )

        if response.status_code == 200:
            return response.json()
        return None

    def get_now_playing(
        self, page: int = 1, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        """
        Get a list of '_media_type' in theatres or TV depends on '_media_type'.
        :param page: page number. Default is 1
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
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

    def get_trending_by_time(
        self,
        time_window: str,
        page: int = 1,
        language: str = "en-US",
        region: str = "US",
    ) -> dict | None:
        """
        Get a list of the current trending '_media_type' on TMDB.
        :param time_window: time window. Default is "day" TODO: change to enum
        :param page: page number. Default is 1
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"trending/{self._media_type}/" + time_window,
            params={
                "api_key": config.api_key,
                "language": language,
                "page": page,
                "region": region.upper(),
            },
        )

        return response.json()

    def get_credits(
        self, content_id: int, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        """
        Get the cast and crew for a '_media_type'.
        :param content_id: content id
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"{self._media_type}/{content_id}/credits",
            params={
                "api_key": config.api_key,
                "language": language,
                "region": region.upper(),
            },
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
        """
        Get a list of recommended '_media_type' for a '_media_type'.
        :param content_id: content id
        :param page: page number. Default is 1
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"{self._media_type}/{content_id}/recommendations",
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

    def get_similar(
        self,
        content_id: int,
        page: int = 1,
        language: str = "en-US",
        region: str = "US",
    ) -> dict | None:
        """
        Get a list of similar '_media_type' for a '_media_type'.
        :param content_id: content id
        :param page: page number. Default is 1
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"{self._media_type}/{content_id}/similar",
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

    def get_provider(
        self, content_id: int, country_code: str = "US", language: str = "en-US"
    ) -> dict | None:
        """
        Get a list of the availabilities per country by provider.
        :param content_id: content id
        :param country_code: country code. Default is "US"
        :param language: language. Default is "en-US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"{self._media_type}/{content_id}/watch/providers",
            params={
                "api_key": config.api_key,
                "language": language,
                "region": country_code,
            },
        )

        if response.status_code == 200:
            try:
                return response.json()["results"][country_code.upper()]
            except KeyError:
                return None

        return None

    def search(
        self, query: str, page: str = 1, language: str = "en-US", region: str = "US"
    ) -> dict | None:
        """
        Search for a '_media_type' by query.
        :param query: query
        :param page: page number. Default is 1
        :param language: language. Default is "en-US"
        :param region: region. Default is "US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"search/{self._media_type}",
            params={
                "api_key": config.api_key,
                "language": language,
                "query": query,
                "region": region.upper(),
                "page": page,
            },
        )

        if response.status_code == 200:
            return response.json()
        return None

    def get_genres(self, language: str = "en-US") -> dict | None:
        """
        Get a list of genres for a '_media_type'.
        :param language: language. Default is "en-US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"genre/{self._media_type}/list",
            params={"api_key": config.api_key, "language": language},
        )

        if response.status_code == 200:
            return response.json()
        return None

    def get_content_by_genre(
        self, genre_ids: str, page: int = 1, language: str = "en-US"
    ) -> dict | None:
        """
        Get a list of content by genre.
        :param genre_ids: genre ids
        :param page: page number. Default is 1
        :param language: language. Default is "en-US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """

        response = requests.get(
            url=self._URL + f"discover/{self._media_type}",
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
        """
        Get a list of videos for a '_media_type'.
        :param content_id: content id
        :param language: language. Default is "en-US"
        :return: dict | None if response status code is not 200 (something went wrong)
        """
        response = requests.get(
            url=self._URL + f"{self._media_type}/{content_id}/videos",
            params={"api_key": config.api_key, "language": language},
        )

        if response.status_code == 200:
            return response.json()
        return None
