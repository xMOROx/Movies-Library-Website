import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import {
  HttpClient,
  HttpHeaders,
  HttpErrorResponse,
} from '@angular/common/http';
import { Router } from '@angular/router';
import { User } from '../models/User';
import jwt_decode from 'jwt-decode';




const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUser: any = {}
  private endpoint: string = 'http://localhost:8080/api/v1/auth';
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };
  constructor(private http: HttpClient, public router: Router) { }

  public singUp(user: User): Observable<any> {
    let url = `${this.endpoint}/register-user`;
    return this.http.post(url, user).pipe(catchError(this.handleError));
  }

  public signIn(user: User): any {
    return this.http.
      post<any>(`${this.endpoint}/signin`, user)
      .subscribe((res: any) => {
        if (res.access == null) {
          alert("Invalid credentials");
          return;
        }

        let decode_token = this.getDecodedAccessToken(res.access);
        localStorage.setItem('access_token', res.access);

        this.getUserProfile(decode_token.user_id).subscribe((res) => {
          this.currentUser = res;
          this.router.navigate(['user-profile/' + res.id]);
        });
      });
  }

  public getUserProfile(id: number): Observable<any> {
    let api = `${this.endpoint}/users/${id}`;
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      "Authorization": "Bearer " + localStorage.getItem('access_token')
    });
    this.httpOptions = {
      headers: headers
    };

    return this.http.get(api, this.httpOptions).pipe(
      map((res) => {
        return res || {}
      }),
      catchError(this.handleError)
    )
  }

  public isLoggedIn(): boolean {
    let authToken = localStorage.getItem('access_token');
    return (authToken !== null) ? true : false;
  }

  public getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  public logout(): void {
    if (localStorage.removeItem('access_token') == null) {
      this.router.navigate(['login']);
    }
  }

  public handleError(error: HttpErrorResponse) {
    let msg = '';
    if (error.error instanceof ErrorEvent) {
      msg = error.error.message;
    } else {
      msg = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    return throwError(() => new Error(msg));
  }

  public getDecodedAccessToken(token: string): any {
    try {
      return jwt_decode(token);
    } catch (Error) {
      return null;
    }
  }
}


