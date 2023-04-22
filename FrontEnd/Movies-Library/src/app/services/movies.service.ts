import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "./auth.service";
import {User} from "../models/User";
import {environment} from "../../environments/environment";
import {Movie} from "../models/Movie";
import {Observable, of, tap} from "rxjs";
import {AggregatedMovie} from "../models/AggregatedMovie";

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  private movieList?: AggregatedMovie[];
  private endpoint: string = `${environment.backEnd}api/v1/`;
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      "Authorization": "Bearer " + localStorage.getItem('access_token')
    })
  };

  public parseMovie(movie: any): Movie {
    return {
      movie_id: movie.id,
      movie_title: movie.title,
      overview: movie.overview,
      genres: movie.genres,
      poster_path: environment.posterPath + movie.poster_path,
      release_date: movie.release_date,
      runtime: movie.runtime
    } as Movie;
  }

  constructor(private http: HttpClient, private auth: AuthService) { }

  public getUserMovies(id: any): Observable<AggregatedMovie[]> {
    if (this.movieList) {
      return of(this.movieList);
    } else {
      return this.http.get<AggregatedMovie[]>(`${this.endpoint}users/${id}/movies/details`, this.httpOptions).pipe(
        tap((movies: AggregatedMovie[]) => {
          this.movieList = movies;
        })
      );
    }
  }

  public getMovieById(id: any) {
    return this.http.get(`${this.endpoint}movies/${id}`, this.httpOptions);
  }

  public getMovieDetailsForUser(movie_id: any, user_id: any) {
    return this.http.get(`${this.endpoint}users/${user_id}/movies/${movie_id}/details`, this.httpOptions);
  }

  public addMovieToUser(movie_id: any, user_id: any, body: any) {
    return this.http.put(`${this.endpoint}users/${user_id}/movies/${movie_id}`, body, this.httpOptions);
  }

}
