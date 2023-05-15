import { Component, OnInit } from '@angular/core';
import { MoviesService } from "src/app/features/services/movies.service";
import { AggregatedMovieModel } from "src/app/features/modules/content/models/AggregatedMovie.model"
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
  private count?: number;
  public page: number;

  constructor(private moviesService: MoviesService, private storageService: StorageService) {
    this.page = 1;
  }

  ngOnInit(): void {
    this.currentUser = this.storageService.getUser();
    this.getMovies(1);

  }

  public getMovies(page: any) {
    this.moviesService.getUserMovies(this.currentUser.id, false, page).subscribe((response: any) => {
      this.count = response.count;
      this.movieList = response.results;
      this.movieList?.forEach((movie: AggregatedMovieModel) => {
        movie.movie.poster_url = environment.posterPath + movie.movie.poster_url;
      });
    });
  }
}
