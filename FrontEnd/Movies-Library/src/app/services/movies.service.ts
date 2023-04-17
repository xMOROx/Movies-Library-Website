import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  private endpoint: string = 'http://localhost:8080/api/v1/';
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      "Authorization": "Bearer " + localStorage.getItem('access_token')
    })
  };

  constructor(private http: HttpClient) { }

  public getMovieById(id: any) {
    return this.http.get(`${this.endpoint}movies/${id}`, this.httpOptions);
  }
}
