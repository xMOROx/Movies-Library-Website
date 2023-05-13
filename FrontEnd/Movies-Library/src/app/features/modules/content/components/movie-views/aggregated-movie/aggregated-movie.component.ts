import { Component, Input } from '@angular/core';
import { AggregatedMovieModel } from "src/app/features/modules/content/models/AggregatedMovie.model";

@Component({
  selector: 'app-aggregated-movie',
  templateUrl: './aggregated-movie.component.html',
  styleUrls: ['./aggregated-movie.component.scss']
})
export class AggregatedMovieComponent {
  @Input() movie!: AggregatedMovieModel;

  constructor() {
  }


}
