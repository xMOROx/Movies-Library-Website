import { Injectable } from '@angular/core';
import {environment} from "../../../environments/environment";
import {TvModel} from "../modules/content/models/Tv.model";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "../../authentication/services/auth.service";
import {Observable, of} from "rxjs";
import {StorageService} from "../../authentication/services/storage.service";

@Injectable({
  providedIn: 'root'
})
export class TvShowsService {
  private endpoint: string = `${environment.backEnd}api/v1/`;
  private language: string = "en-US";
  private region: string = "US";

  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      "Authorization": "Bearer " + localStorage.getItem('access_token')
    })
  };

  public parseTv(tv: any): TvModel {
    return {
      original_name: tv.original_name,
      name: tv.name,
      tagline: tv.tagline,
      popularity: tv.populatiry,
      vote_count: tv.vote_count,
      first_air_date: tv.first_air_date,
      backdrop_path: environment.backdropPath + tv.backdrop_path,
      original_language: tv.original_language,
      id: tv.id,
      vote_average: tv.vote_average,
      overview: tv.overview,
      poster_path: tv.poster_path,
      created_by: tv.created_by,
      genres: tv.genres,
      homepage: tv.homepage,
      number_of_episodes: tv.number_of_episodes,
      number_of_seasons: tv.number_of_seasons,
      seasons: tv.seasons,
      origin_country: tv.origin_country
    } as TvModel;
  }

  constructor(private http: HttpClient, private auth: AuthService, private storage: StorageService) { }

  public getUserTvShows(id: any, all: boolean = false, page: any = 1): Observable<any> {
    if (!this.auth.isAuthenticated().subscribe((res: any) => res)) {
      return of(null);
    }

    return this.http.get(`${this.endpoint}users/${id}/tv?all=${all}&page=${page}`, this.httpOptions);
  }

  public getTvDetailsForUser(tv_id: any, user_id: any): Observable<any> {
    if (!this.auth.isAuthenticated().subscribe((res: any) => res)) {
      return of(null);
    }

    return this.http.get(`${this.endpoint}users/${user_id}/tv/${tv_id}/details`, this.httpOptions);
  }

  public addTvToUser(tv_id: any, user_id: any, body: any): Observable<any> {
    if (!this.auth.isAuthenticated().subscribe((res: any) => res)) {
      return of(null);
    }
    return this.http.put(`${this.endpoint}users/${user_id}/tv/${tv_id}`, body, this.httpOptions);
  }

  public getTvById(id: any): Observable<any> {
    return this.http.get(`${this.endpoint}tv/${id}?language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public getPopularTv(page: number): Observable<any> {
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/popular?page=${page}&language=${this.language}&region=${this.region}&user=${user}`, this.httpOptions);
  }

  public getUpcomingTv(page: number, timeWindow: string): Observable<any> {
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/upcoming?page=${page}&language=${this.language}&region=${this.region}&time_window=${timeWindow}&user=${user}`, this.httpOptions);
  }

  public getLatestTv(page: number): Observable<any> {
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/latest?page=${page}&language=${this.language}&region=${this.region}&user=${user}`, this.httpOptions);
  }

  public getTrendingTv(page: number, timeWindow: string): Observable<any> {
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/trending?page=${page}&language=${this.language}&region=${this.region}&time_window=${timeWindow}&user=${user}`, this.httpOptions);
  }

  public getAiringToday(page: number): Observable<any> {
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/airing_today?page=${page}&language=${this.language}&region=${this.region}&user=${user}`, this.httpOptions);
  }

  public getAiringThisWeek(page: number): Observable<any> {
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/airing_this_week?page=${page}&language=${this.language}&region=${this.region}&user=${user}`, this.httpOptions);
  }

  public searchTv(searchQuery: string, page: number): Observable<any> {
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/search?query=${searchQuery}&page=${page}&language=${this.language}&region=${this.region}&user=${user}`, this.httpOptions);
  }

  public getGenres(): Observable<any> {
    return this.http.get(`${this.endpoint}tv/genres?language=${this.language}`, this.httpOptions);
  }

  public getTvByGenreId(id: string[], page: any = 1): Observable<any> {
    let genres = '';
    id.forEach((genre_id) => {
      genres += genre_id + ','
    });
    genres = genres.slice(0, -1);
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/with?genres=${genres}&page=${page}&language=${this.language}&user=${user}`, this.httpOptions);
  }

  public getTvCredits(id: string): Observable<any> {
    return this.http.get(`${this.endpoint}tv/${id}/credits?language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public getTvVideos(id: string): Observable<any> {
    return this.http.get(`${this.endpoint}tv/${id}/videos?language=${this.language}&region=${this.region}`, this.httpOptions);
  }

  public getRecommendedTv(id: string, page: number): Observable<any> {
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/${id}/recommendations?language=${this.language}&region=${this.region}&page=${page}&user=${user}`, this.httpOptions);
  }

  public getSimilarTv(id: string, page: number): Observable<any> {
    let user = -1;
    if (this.storage.getUser()) {
      user = this.storage.getUser().id;
    }
    return this.http.get(`${this.endpoint}tv/${id}/similar?language=${this.language}&region=${this.region}&page=${page}&user=${user}`, this.httpOptions);
  }

  public getTvProviders(id: string): Observable<any> {
    return this.http.get(`${this.endpoint}tv/${id}/providers?language=${this.language}&region=${this.region}`, this.httpOptions);
  }
}
