import {Component, OnInit} from '@angular/core';
import {Movie} from "../../models/Movie";
import {MoviesService} from "../../services/movies.service";
import {ActivatedRoute} from "@angular/router";
import {User} from "../../models/User";
import {AuthService} from "../../services/auth.service";
import {catchError} from "rxjs/operators";
import {throwError} from "rxjs";

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  public movie?: Movie;
  public status?: string;
  public user?: User;

  constructor(private moviesService: MoviesService, private route: ActivatedRoute, private auth: AuthService) {
  }

  ngOnInit(): void {
    this.moviesService.getMovieById(this.route.snapshot.paramMap.get('id')).subscribe((res: any) => {
      this.movie = res;
      this.auth.getUserProfile(localStorage.getItem('user_id')).subscribe((user: User) => {
        this.user = user;
        this.moviesService.getMovieDetailsForUser(this.movie?.movie_id, user.id)?.pipe(catchError(err => {
          this.status = "Not watched";
          return throwError(err);
        })).subscribe((data: any) => {
          this.status = data.status;
        });
      });
    });
  }

  public getRuntime(runtime: number): string {
    if (Math.floor(runtime/60) == 0) {
      return runtime.toString();
    } else {
      return Math.floor(runtime/60).toString() + 'h ' + (runtime % 60).toString() + 'min';
    }
  }

  public addMovie() {
    this.moviesService.addMovieToUser(this.movie?.movie_id, this.user?.id, this.status).subscribe(res => {
      console.log(res);
    });
  }

}
