import {Injectable} from '@angular/core';
import {Observable, throwError} from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import {
  HttpClient,
  HttpHeaders,
  HttpErrorResponse, HttpResponse,
} from '@angular/common/http';
import {Router} from '@angular/router';
import {User} from '../models/User';
import jwt_decode from 'jwt-decode';
import {TokenService} from "./token.service";
import {environment} from "../../environments/environment";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUser: any = {}
  private endpoint: string = `${environment.backEnd}api/v1/auth`;
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(private http: HttpClient, public router: Router, private tokenService: TokenService) {
  }

  public singUp(user: User): Observable<any> {
    let url = `${this.endpoint}/register-user`;
    return this.http.post<any>(url, user).pipe(catchError(this.handleError));
  }

  public signIn(user: User): any {
    return this.http.post<any>(`${this.endpoint}/signin`, user)
      .subscribe((res: any) => {
        if (res.access == null) {
          alert("Invalid credentials");
          return;
        }
        let decode_token = this.tokenService.getDecodedAccessToken(res.access);
        localStorage.setItem('access_token', res.access);
        localStorage.setItem('refresh_token', res.refresh);

        this.getUserProfile(decode_token.user_id).subscribe((res: User) => {
          this.currentUser = res;
          if (res !== undefined) {
            localStorage.setItem('user_id', <string>res.id);
          }
          this.router.navigate(['user-profile/' + res.id]);
        });
      });
  }


  public getUserProfile(id: any): Observable<any> {
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
    return (authToken !== null);
  }

  public logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id')
    this.router.navigate(['login']);
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

  public refreshToken(token: string) {
    return this.http.post(`${this.endpoint}/token/refresh`, {"refresh": token});
  }
}
