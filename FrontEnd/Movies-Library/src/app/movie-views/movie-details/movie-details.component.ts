import { Component, OnInit } from '@angular/core';
import { Movie } from "../../models/Movie";
import { MoviesService } from "../../services/movies.service";
import { ActivatedRoute } from "@angular/router";
import { User } from "../../models/User";
import { AuthService } from "../../services/auth.service";
import { catchError } from "rxjs/operators";
import { throwError } from "rxjs";
import { StorageService } from 'src/app/services/storage.service';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  public movie?: Movie;
  public status?: string;
  public user?: User;

  constructor(private moviesService: MoviesService, private route: ActivatedRoute, private storage: StorageService) {
  }

  ngOnInit(): void {
    this.user = this.storage.getUser();

    if (this.user == null) {
      return;
    }

    this.moviesService.getMovieById(this.route.snapshot.paramMap.get('id')).subscribe((res: any) => {
      this.movie = res;

      this.moviesService.getMovieDetailsForUser(this.movie?.movie_id, this.user!.id)?.pipe(catchError(err => {
        this.status = "Not watched";
        return throwError(() => new Error(err));
      })).subscribe((data: any) => {
        this.status = data.status;
      });
    });
  }

  public getRuntime(runtime: number): string {
    if (Math.floor(runtime / 60) == 0) {
      return runtime.toString();
    } else {
      return Math.floor(runtime / 60).toString() + 'h ' + (runtime % 60).toString() + 'min';
    }
  }

  public addMovie() {
    this.moviesService.addMovieToUser(this.movie?.movie_id, this.user?.id, this.status).subscribe(res => {
      console.log(res);
    });
  }

}
