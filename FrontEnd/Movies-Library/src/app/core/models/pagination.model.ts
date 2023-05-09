import { AggregatedMovieModel } from "src/app/features/content/models/AggregatedMovie.model";
import { MovieModel } from "src/app/features/content/models/Movie.model";
import { TvModel } from "src/app/features/content/models/tv.model";

export interface PaginationModel {
    dates?: Object;
    page: number;
    results: Array<MovieModel | TvModel | AggregatedMovieModel>;
    total_pages: number;
    total_results: number;
}