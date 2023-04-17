import {Component, OnInit} from '@angular/core';
import {Movie} from "../../models/Movie";
import {MoviesService} from "../../services/movies.service";
import {ActivatedRoute} from "@angular/router";
import {User} from "../../models/User";
import {AuthService} from "../../services/auth.service";
import {catchError} from "rxjs/operators";
import {throwError} from "rxjs";
import {environment} from "../../../environments/environment";
import { StorageService } from 'src/app/services/storage.service';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  public movie?: Movie;
  public status?: string;
  public rating?: any;
  public is_favorite?: boolean;
  public user?: User;

  constructor(private moviesService: MoviesService, private route: ActivatedRoute, private storage: StorageService) {
  }

  ngOnInit(): void {
    this.user = this.storage.getUser();

    if (this.user == null) {
      return;
    }

    this.moviesService.getMovieById(this.route.snapshot.paramMap.get('id')).subscribe((res: any) => {
      this.movie = this.moviesService.parseMovie(res);
      this.moviesService.getMovieDetailsForUser(this.movie?.movie_id, this.user!.id)?.pipe(catchError(err => {
        this.status = "Not watched";
        return throwError(() => new Error(err));
      })).subscribe((data: any) => {
        this.status = data.status;
        this.rating = data.rating;
        this.is_favorite = data.is_favorite;
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
    let body = {
      "status": this.status,
      "rating": this.rating,
      "is_favorite": this.is_favorite
    };
    this.moviesService.addMovieToUser(this.movie?.movie_id, this.user?.id, body).subscribe();
  }

}
