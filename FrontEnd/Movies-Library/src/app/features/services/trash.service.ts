import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {Observable, of, tap} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class TrashService {
  private endpoint: string = `${environment.backEnd}api/v1/trash/`;
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      "Authorization": "Bearer " + localStorage.getItem('access_token')
    })
  };
  private movies?: Array<number>;

  constructor(private http: HttpClient) { }

  public getMovieById(user_id: any, movie_id: any): Observable<any> {
    return this.http.get(`${this.endpoint}user/${user_id}/movies/${movie_id}` ,this.httpOptions);
  }

  public getMoviesForUser(user_id: any): Observable<Array<number>> {
    if (this.movies) {
      return of(this.movies);
    }
    return this.http.get<Array<number>>(`${this.endpoint}user/${user_id}/movies`, this.httpOptions).pipe(
      tap(movies => {
        this.movies = movies;
      })
    );
  }

  public addMovieToTrash(user_id: any, movie_id: any): Observable<any> {
    return this.http.post(`${this.endpoint}user/${user_id}/movies/${movie_id}/add`, {}, this.httpOptions);
  }

  public deleteMovieFromTrash(user_id: any, movie_id: any): Observable<any> {
    return this.http.delete(`${this.endpoint}user/${user_id}/movies/${movie_id}/delete`, this.httpOptions);
  }
}
