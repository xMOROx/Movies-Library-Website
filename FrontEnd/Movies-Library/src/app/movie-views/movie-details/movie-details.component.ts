import {Component, OnInit} from '@angular/core';
import {Movie} from "../../models/Movie";
import {MoviesService} from "../../services/movies.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  public movie?: Movie;

  constructor(private moviesService: MoviesService, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.moviesService.getMovieById(this.route.snapshot.paramMap.get('id')).subscribe((res: any) => {
      this.movie = res;
    });
  }

  public getRuntime(runtime: number): string {
    if (Math.floor(runtime/60) == 0) {
      return runtime.toString();
    } else {
      return Math.floor(runtime/60).toString() + 'h ' + (runtime % 60).toString() + 'min';
    }
  }

  public addMovie(status: string) {

  }

}
