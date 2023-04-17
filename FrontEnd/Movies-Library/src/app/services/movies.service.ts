import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "./auth.service";
import {User} from "../models/User";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  private endpoint: string = `${environment.backEnd}api/v1/`;
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      "Authorization": "Bearer " + localStorage.getItem('access_token')
    })
  };

  constructor(private http: HttpClient, private auth: AuthService) { }

  public getMovieById(id: any) {
    return this.http.get(`${this.endpoint}movies/${id}`, this.httpOptions);
  }

  public getMovieDetailsForUser(movie_id: any, user_id: any) {
    return this.http.get(`${this.endpoint}users/${user_id}/movies/${movie_id}/details`, this.httpOptions);
  }

  public addMovieToUser(movie_id: any, user_id: any, status: any) {
    return this.http.post(`${this.endpoint}users/${user_id}/movies/${movie_id}`, {"status": status}, this.httpOptions);
  }
}
