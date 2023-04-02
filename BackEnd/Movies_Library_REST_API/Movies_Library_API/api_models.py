class MovieDetails:
    _POSTER_URL = "https://image.tmdb.org/t/p/original"

    def __init__(self, movie_id, movie_title, overview, genres, poster_path, release_date, runtime):
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.overview = overview
        self.genres = genres  # genre array
        if poster_path is not None:
            self.poster_path = self._POSTER_URL + poster_path
        else:
            self.poster_path = None
        self.release_date = release_date  # yyyy-mm-dd
        self.runtime = runtime  # in minutes


class Genre:
    def __init__(self, genre_id, genre_name):
        self.genre_id = genre_id
        self.genre_name = genre_name
