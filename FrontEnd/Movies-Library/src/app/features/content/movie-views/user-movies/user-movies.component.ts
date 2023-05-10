import { Component, OnInit } from '@angular/core';
import { MoviesService } from "src/app/features/services/movies.service";
import { AggregatedMovieModel } from "src/app/features/content/models/AggregatedMovie.model"
import { StorageService } from "src/app/authentication/services/storage.service";
import { User } from "src/app/authentication/models/User";
import { environment } from "src/environments/environment";

@Component({
  selector: 'app-user-movies',
  templateUrl: './user-movies.component.html',
  styleUrls: ['./user-movies.component.scss']
})
export class UserMoviesComponent implements OnInit {

  public movieList?: Array<AggregatedMovieModel>;
  public currentUser: User = {
    email: '',
    first_name: '',
    last_name: '',
    password: '',
  };
  public filter = "all";

  constructor(private moviesService: MoviesService, private storageService: StorageService) {
  }

  ngOnInit(): void {
    this.currentUser = this.storageService.getUser();
    this.moviesService.getUserMovies(this.currentUser.id).subscribe((movies: Array<AggregatedMovieModel>) => {
      this.movieList = movies;
      this.movieList.forEach((movie: AggregatedMovieModel) => {
        movie.movie.poster_url = environment.posterPath + movie.movie.poster_url;
      });
    });
  }
}
