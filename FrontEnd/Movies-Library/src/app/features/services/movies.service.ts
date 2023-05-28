import { Injectable, ModuleWithProviders } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { AuthService } from "src/app/authentication/services/auth.service";
import { environment } from "src/environments/environment";
import { MovieModel } from "src/app/features/modules/content/models/Movie.model";
import { Observable, of, tap } from "rxjs";
import { AggregatedMovieModel } from "src/app/features/modules/content/models/AggregatedMovie.model";

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  private movieList?: Array<AggregatedMovieModel>;

  private endpoint: string = `${environment.backEnd}api/v1/`;
  private language: string = "en-US";
  private region: string = "US";

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
      poster_path: movie.poster_path,
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

  public getUserMovies(id: any, all: boolean = false, page: any = 1): Observable<any> {
    if (!this.auth.isAuthenticated().subscribe((res: any) => res)) {
      return of(null);
    }

    // if (this.movieList) {
    //   return of(this.movieList);
    // }

    return this.http.get(`${this.endpoint}users/${id}/movies?all=${all}&page=${page}`, this.httpOptions);
  // .pipe(
  //     tap((response: any) => {
  //       if (all) {
  //         this.movieList = response;
  //       }
  //     })
  //   )

  }

  public getMovieDetailsForUser(movie_id: any, user_id: any): Observable<any> {
    if (!this.auth.isAuthenticated().subscribe((res: any) => res)) {
      return of(null);
    }
    return this.http.get(`${this.endpoint}users/${user_id}/movies/${movie_id}/details`, this.httpOptions);
  }

  public addMovieToUser(movie_id: any, user_id: any, body: any): Observable<any> {
    if (!this.auth.isAuthenticated().subscribe((res: any) => res)) {
      return of(null);
    }
    return this.http.put(`${this.endpoint}users/${user_id}/movies/${movie_id}`, body, this.httpOptions);
  }

  // general movies
  public getMovieById(id: any): Observable<any> {
    return this.http.get(`${this.endpoint}movies/${id}?language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public getPopularMovies(page: number): Observable<any> {
    return this.http.get(`${this.endpoint}movies/popular?page=${page}&language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public getUpcomingMovies(page: number, timeWindow: string): Observable<any> {
    return this.http.get(`${this.endpoint}movies/upcoming?page=${page}&language=${this.language}&region=${this.region}&time_window=${timeWindow}`, this.httpOptions);
  }

  public getLatestMovies(page: number): Observable<any> {
    return this.http.get(`${this.endpoint}movies/latest?page=${page}&language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public getTrendingMovies(page: number, timeWindow: string): Observable<any> {
    return this.http.get(`${this.endpoint}movies/trending?page=${page}&language=${this.language}&region=${this.region}&time_window=${timeWindow}`, this.httpOptions);
  }

  public getNowPlayingMovies(page: number): Observable<any> {
    return this.http.get(`${this.endpoint}movies/now_playing?page=${page}&language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public searchMovies(searchQuery: string, page: number): Observable<any> {
    return this.http.get(`${this.endpoint}movies/search?query=${searchQuery}&page=${page}&language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public getGenres(): Observable<any> {
    return this.http.get(`${this.endpoint}movies/genres?language=${this.language}`, this.httpOptions);
  }

  public getMoviesByGenreId(id: string[], page: any = 1): Observable<any> {
    let genres = '';
    id.forEach((genre_id) => {
      genres += genre_id + ','
    });
    genres = genres.slice(0, -1);

    return this.http.get(`${this.endpoint}movies/with?genres=${genres}&page=${page}&language=${this.language}`, this.httpOptions);
  }

  public getMovieCredits(id: string): Observable<any> {
    return this.http.get(`${this.endpoint}movies/${id}/credits?language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public getMovieVideos(id: string): Observable<any> {
    return this.http.get(`${this.endpoint}movies/${id}/videos?language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public getRecommendedMovies(id: string, page: number): Observable<any> {
    return this.http.get(`${this.endpoint}movies/${id}/recommendations?language=${this.language}&region=${this.region}&page=${page}`, this.httpOptions);
  }

  public getSimilarMovies(id: string, page: number): Observable<any> {
    return this.http.get(`${this.endpoint}movies/${id}/similar?language=${this.language}&region=${this.region}&page=${page}`, this.httpOptions);
  }

  public getMovieProviders(id: string): Observable<any> {
    return this.http.get(`${this.endpoint}movies/${id}/providers?language=${this.language}&region=${this.region}`, this.httpOptions);
  }


}
