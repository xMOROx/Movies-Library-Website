export interface AggregatedMovie {
  status: string;
  rating?: number;
  is_favorite: boolean;
  movie: {
    id: string;
    poster_url: string;
    runtime: number;
    title: string;
  };
};
