import { Component, Input } from '@angular/core';
import { AggregatedMovie } from "src/app/models/AggregatedMovie";

@Component({
  selector: 'app-aggregated-movie',
  templateUrl: './aggregated-movie.component.html',
  styleUrls: ['./aggregated-movie.component.scss']
})
export class AggregatedMovieComponent {
  @Input() movie!: AggregatedMovie;

  constructor() {
  }


}
