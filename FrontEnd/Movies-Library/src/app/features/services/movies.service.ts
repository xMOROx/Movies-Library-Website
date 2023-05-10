import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { AuthService } from "src/app/authentication/services/auth.service";
import { User } from "src/app/authentication/models/User";
import { environment } from "src/environments/environment";
import { MovieModel } from "src/app/features/content/models/Movie.model";
import { Observable, of, tap } from "rxjs";
import { AggregatedMovieModel } from "src/app/features/content/models/AggregatedMovie.model";

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  private movieList?: Array<AggregatedMovieModel>;
  private endpoint: string = `${environment.backEnd}api/v1/`;
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      "Authorization": "Bearer " + localStorage.getItem('access_token')
    })
  };

  public parseMovie(movie: any): MovieModel {
    return {
      adult: movie.adult,
      backdrop_path: environment.backdropPath + movie.backdrop_path,
      genres: movie.genres,
      homepage: movie.homepage,
      id: movie.id,
      imdb_id: movie.imdb_id,
      original_language: movie.original_language,
      original_title: movie.original_title,
      overview: movie.overview,
      popularity: movie.popularity,
      poster_path: environment.posterPath + movie.poster_path,
      production_companies: movie.production_companies,
      production_countries: movie.production_countries,
      release_date: movie.release_date,
      revenue: movie.revenue,
      runtime: movie.runtime,
      spoken_languages: movie.spoken_languages,
      status: movie.status,
      tagline: movie.tagline,
      title: movie.title,
      video: movie.video,
      vote_average: movie.vote_average,
      vote_count: movie.vote_count

    } as MovieModel;
  }

  constructor(private http: HttpClient, private auth: AuthService) { }

  public getUserMovies(id: any): Observable<Array<AggregatedMovieModel>> {
    if (this.movieList) {
      return of(this.movieList);
    } else {
      return this.http.get<Array<AggregatedMovieModel>>(`${this.endpoint}users/${id}/movies/details`, this.httpOptions).pipe(
        tap((movies: Array<AggregatedMovieModel>) => {
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
