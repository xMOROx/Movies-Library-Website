import requests
import config
from api_models import MovieDetails, Genre


class MovieRequests:
    _URL = "https://api.themoviedb.org/3/"

    def __convert_json_to_movie(self, json):
        movie_id = json['id']
        movie_title = json['title']
        overview = json['overview']
        genres = []
        for genre in json['genres']:
            genres.append(Genre(genre['id'], genre['name']))
        poster_path = json['poster_path']
        release_date = json['release_date']
        runtime = json['runtime']
        return MovieDetails(movie_id, movie_title, overview, genres, poster_path, release_date, runtime)

    def get_popular_movies(self):
        response = requests.get(url=self._URL + "movie/popular",
                                params={"api_key": config.api_key, "language": "en-US"})
        if response.status_code == 200:
            data = response.json()
            print(data)
            movies = []
            for movie in data['results']:
                movies.append(self.get_movie_details(movie['id']))
            return movies
        return None

    def get_movie_details(self, movie_id):
        response = requests.get(url=self._URL + "movie/" + str(movie_id),
                                params={"api_key": config.api_key, "language": "en-US"})
        if response.status_code == 200:
            data = response.json()
            return self.__convert_json_to_movie(data)
        return None

    def get_upcoming_movies(self):
        response = requests.get(url=self._URL + "movie/upcoming",
                                params={"api_key": config.api_key, "language": "en-US", 'region': 'US'})
        if response.status_code == 200:
            data = response.json()
            movies = []
            for movie in data['results']:
                movies.append(self.get_movie_details(movie['id']))
            return movies
        return None

    def get_latest_movies(self):
        response = requests.get(url=self._URL + "movie/now_playing",
                                params={"api_key": config.api_key, "language": "en-US"})
        if response.status_code == 200:
            data = response.json()
            movies = []
            for movie in data['results']:
                movies.append(self.get_movie_details(movie['id']))
            return movies
        return None

    def get_movies_by_query(self, query):
        response = requests.get(url=self._URL + "search/movie",
                                params={"api_key": config.api_key, "language": "en-US", 'query': query})
        if response.status_code == 200:
            data = response.json()
            movies = []
            for movie in data['results']:
                movies.append(self.get_movie_details(movie['id']))
            return movies
        return None
