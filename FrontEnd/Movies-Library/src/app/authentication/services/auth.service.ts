import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import {
  HttpClient,
  HttpHeaders,
  HttpErrorResponse,
} from '@angular/common/http';
import { Router } from '@angular/router';
import { User } from '../../models/User';
import { TokenService } from "./token.service";
import { environment } from "../../../environments/environment";
import { StorageService } from './storage.service';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private endpoint: string = `${environment.backEnd}api/v1/auth`;
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(
    private http: HttpClient,
    private router: Router,
    private tokenService: TokenService,
    private storageService: StorageService
  ) {
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

        this.tokenService.createToken(res.access, res.refresh);

        this.getUserProfile(decode_token.user_id).subscribe((res) => {
          this.storageService.saveUser(res);
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
    return !!this.tokenService.getAccessToken();
  }

  public logout(): void {
    if (this.tokenService.removeAccessToken()) {
      this.storageService.clean();
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

  public refreshToken(refresh: string) {
    return this.http.post(`${this.endpoint}/token/refresh`, { "refresh": refresh });
  }
}
