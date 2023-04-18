import {Component, OnInit} from '@angular/core';
import {MoviesService} from "../../services/movies.service";
import {AggregatedMovie} from "../../models/AggregatedMovie";
import {StorageService} from "../../services/storage.service";
import {User} from "../../models/User";
import {environment} from "../../../environments/environment";

@Component({
  selector: 'app-user-movies',
  templateUrl: './user-movies.component.html',
  styleUrls: ['./user-movies.component.css']
})
export class UserMoviesComponent implements OnInit {

  public movieList?: AggregatedMovie[];
  public currentUser: User = {
    email: '',
    first_name: '',
    last_name: '',
    password: '',
  };

  constructor(private moviesService: MoviesService, private storageService: StorageService) {
  }

  ngOnInit(): void {
    this.currentUser = this.storageService.getUser();
    this.moviesService.getUserMovies(this.currentUser.id).subscribe((movies: AggregatedMovie[]) => {
      this.movieList = movies;
      this.movieList.forEach((movie: AggregatedMovie) => {
        movie.movie.poster_url = environment.posterPath + movie.movie.poster_url;
      });
    });
  }

}
