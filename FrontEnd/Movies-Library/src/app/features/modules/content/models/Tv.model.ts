import { Genre } from "./Genre.model";

export interface TvModel {
    original_name: string;
    name: string;
    tagline: string;
    popularity: number;
    origin_country: Array<string>;
    vote_count: number;
    first_air_date: string;
    backdrop_path: string;
    original_language: string;
    id: number;
    vote_average: number;
    overview: string;
    poster_path: string;
    created_by: Array<any>;
    genres: Array<Genre>;
    homepage: string;
    number_of_episodes: number;
    number_of_seasons: number;
    seasons: Array<any>;
}
