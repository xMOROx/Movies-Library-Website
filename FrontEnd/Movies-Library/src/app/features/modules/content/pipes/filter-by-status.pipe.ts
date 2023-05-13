import { Pipe, PipeTransform } from '@angular/core';
import { AggregatedMovieModel } from "src/app/features/modules/content/models/AggregatedMovie.model";

@Pipe({
  name: 'filterByStatus'
})
export class FilterByStatusPipe implements PipeTransform {

  transform(movies: Array<AggregatedMovieModel>, status: string): Array<AggregatedMovieModel> {
    if (status === "all") {
      return movies;
    }
    return movies.filter(movie => movie.status == status);
  }

}
