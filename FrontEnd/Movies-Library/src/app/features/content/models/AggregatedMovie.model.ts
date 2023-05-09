export interface AggregatedMovieModel {
  status: string;
  rating?: number;
  is_favorite: boolean;
  movie: Movie;
};

interface Movie {
  id: string;
  poster_url: string;
  runtime: number;
  title: string;
};
