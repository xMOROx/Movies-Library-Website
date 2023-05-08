import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/models/User';
import { AuthService } from 'src/app/authentication/services/auth.service';
import { StorageService } from 'src/app/authentication/services/storage.service';
import { MoviesService } from "src/app/core/services/movies.service";
import { AggregatedMovie } from "src/app/models/AggregatedMovie";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

  private movieList?: AggregatedMovie[];

  public currentUser: User = {
    email: '',
    first_name: '',
    last_name: '',
    password: '',
  };
  constructor(
    public authService: AuthService,
    private storageService: StorageService,
    private moviesService: MoviesService
  ) { }

  ngOnInit() {
    this.currentUser = this.storageService.getUser();
    this.moviesService.getUserMovies(this.currentUser.id).subscribe((movies: AggregatedMovie[]) => {
      this.movieList = movies;
    });
  }

  public getWatchTime(): string {
    let runtime_sum = 0;
    this.movieList?.forEach((movie: AggregatedMovie) => {
      if (movie.status === "Watched" && movie.movie.runtime) {
        runtime_sum += movie.movie.runtime;
      }
    });
    let result = ""
    if (Math.floor(runtime_sum / 1440) > 0) {
      result += Math.floor(runtime_sum / 1440).toString() + "days ";
      runtime_sum %= 1440;
    }
    if (Math.floor(runtime_sum / 60) > 0) {
      result += Math.floor(runtime_sum / 60).toString() + "h ";
    }
    return result + (runtime_sum % 60).toString() + "min";
  }

}
