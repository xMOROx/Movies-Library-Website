import { Component, OnInit } from '@angular/core';
import { ActorModel } from 'src/app/features/modules/actors/models/Actor.model';
import { MovieModel } from 'src/app/features/modules/content/models/Movie.model';
import { ActivatedRoute } from '@angular/router';
import { ActorsService } from '../../services/actors.service';

@Component({
  selector: 'app-actor',
  templateUrl: './actor.component.html',
  styleUrls: ['./actor.component.scss']
})
export class ActorComponent implements OnInit {
  public actor: ActorModel | null = null;
  public movies: Array<MovieModel> = [];
  public externalIds: Array<any> = [];
  constructor(
    private router: ActivatedRoute,
    private actorsService: ActorsService
  ) { }

  ngOnInit() {
    this.router.params.subscribe(params => {
      const id = params['id'];
      this.actorsService.getActorDetails(id).subscribe((data: ActorModel) => {
        this.actor = data;
      });

      this.actorsService.getActorExternalData(id).subscribe((data: any) => {
        this.externalIds = data;
      });

      this.actorsService.getActorCast(id).subscribe((data: any) => {
        this.movies = data.cast;
      });
    });

  }

}
