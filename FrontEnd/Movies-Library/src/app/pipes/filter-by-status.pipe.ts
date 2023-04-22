import { Pipe, PipeTransform } from '@angular/core';
import {AggregatedMovie} from "../models/AggregatedMovie";

@Pipe({
  name: 'filterByStatus'
})
export class FilterByStatusPipe implements PipeTransform {

  transform(movies: AggregatedMovie[], status: string): AggregatedMovie[] {
    if (status === "all") {
      return movies;
    }
    return movies.filter(movie => movie.status == status);
  }

}
