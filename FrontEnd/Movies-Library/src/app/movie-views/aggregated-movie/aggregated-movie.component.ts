import {Component, Input} from '@angular/core';
import {AggregatedMovie} from "../../models/AggregatedMovie";

@Component({
  selector: 'app-aggregated-movie',
  templateUrl: './aggregated-movie.component.html',
  styleUrls: ['./aggregated-movie.component.css']
})
export class AggregatedMovieComponent {
  @Input() movie!: AggregatedMovie;

  constructor() {
  }


}
