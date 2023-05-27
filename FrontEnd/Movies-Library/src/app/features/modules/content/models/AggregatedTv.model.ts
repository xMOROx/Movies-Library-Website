export interface AggregatedTvModel {
  status: string;
  rating?: number;
  is_favorite: boolean;
  tv: Tv;
};

interface Tv {
  id: string;
  poster_url: string;
  title: string;
};
