import { Pipe, PipeTransform } from '@angular/core';
import { ActorModel } from 'src/app/features/modules/actors/models/Actor.model';

@Pipe({
  name: 'popularitySort'
})
export class PopularitySortPipe implements PipeTransform {

  transform(actors: Array<ActorModel>, order?: string, by?: string): Array<ActorModel> {
    if (order === 'asc') {
      if (by === 'popularity') {
        return actors.sort((a, b) => a.popularity - b.popularity);
      }
      else if (by === 'name') {
        return actors.sort((a, b) => a.name.localeCompare(b.name));
      }
    }
    else if (order === 'desc') {
      if (by === 'popularity') {
        return actors.sort((a, b) => b.popularity - a.popularity);
      }
      else if (by === 'name') {
        return actors.sort((a, b) => b.name.localeCompare(a.name));
      }
    }
    return actors;
  }

}
