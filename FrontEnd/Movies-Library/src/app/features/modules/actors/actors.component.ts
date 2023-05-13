import { Component, OnInit } from '@angular/core';
import {PaginationModel} from 'src/app/features/modules/content/models/pagination.model';
import {ActorsService} from "./services/actors.service";
import {take} from "rxjs";
import {PaginationActorModel} from "./models/paginationActor.model";
@Component({
  selector: 'app-actors',
  templateUrl: './actors.component.html',
  styleUrls: ['./actors.component.scss']
})
export class ActorsComponent implements OnInit {

  public actors: Array<PaginationActorModel> = [];

  public totalResults: any;
  constructor(
    private actorsService: ActorsService
  ) { }

  ngOnInit() {
    this.getActors(1);
  }

  public getActors(page: number) {
    this.actorsService.getActors(page).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.actors = response.results;
          this.totalResults = response.total_results;
        },
        error: (_: any) => {
        }
      }
    );
  }

  public changePage(event: any) {
    this.getActors(event.pageIndex + 1);
  }

}
