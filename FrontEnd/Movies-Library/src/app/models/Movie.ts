import {Genre} from "./Genre";

export interface Movie {
  movie_id: string;
  movie_title: string;
  overview: string;
  genres: Genre[];
  poster_path: string;
  release_date: string;
  runtime: number;
};
