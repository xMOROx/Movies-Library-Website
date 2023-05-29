import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import {
  HttpClient,
  HttpHeaders,
  HttpErrorResponse,
} from '@angular/common/http';
import { Router } from '@angular/router';
import { User } from 'src/app/authentication/models/User';
import { TokenService } from "./token.service";
import { environment } from "src/environments/environment";
import { StorageService } from './storage.service';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private endpoint: string = `${environment.backEnd}api/v1/auth`;
  private isAuth: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(!!this.storageService.getUser());
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
    return this.http.post<any>(url, user);
  }

  public signIn(user: User): any {
    return this.http.post<any>(`${this.endpoint}/signin`, user)
      .subscribe(
        {
          next: (res: any) => {
            if (res.access == null) {
              alert("Invalid credentials");
              return;
            }
            let decode_token = this.tokenService.getDecodedAccessToken(res.access);

            this.tokenService.createToken(res.access, res.refresh);

            this.getUserProfile(decode_token.user_id).subscribe((res) => {
              this.storageService.saveUser(res);
              this.isAuth.next(true);
              this.router.navigate(['dashboard/' + res.id]);
            });
          },
          error: (_: HttpErrorResponse) => {
            alert("Invalid credentials");
          }
        }

      );
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
      map((res: any) => {
        return this.parseRoles(res) || {}
      }),
      catchError(this.handleError)
    )
  }

  public parseRoles(res: any): any {
    res['roles'] = {
      admin: res.is_superuser,
      user: true,
      staff: res.is_staff
    };

    delete res['is_superuser'];
    delete res['is_staff'];
    return res;
  }

  public isLoggedIn(): boolean {
    let value = !!this.tokenService.getAccessToken();

    this.isAuth.next(value);
    return value;
  }

  public logout(): void {
    if (this.tokenService.removeAccessToken()) {
      this.storageService.clean();
      this.isAuth.next(false);
      this.router.navigate(['/']);
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

  public isAuthenticated(): Observable<boolean> {
    return this.isAuth.asObservable();
  }

  public changePassword(id: number, body: any): any {
    let api = `${this.endpoint}/users/${id}/change-password`;

    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      "Authorization": "Bearer " + localStorage.getItem('access_token')
    });

    this.httpOptions = {
      headers: headers
    };

    return this.http.put(api, body, this.httpOptions);
  }

  public updateProfile(id: number, body: any): any {
    let api = `${this.endpoint}/users/${id}`;

    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      "Authorization": "Bearer " + localStorage.getItem('access_token')
    });

    this.httpOptions = {
      headers: headers
    };

    return this.http.put(api, body, this.httpOptions);
  }

  public isStaff(): boolean {
    let user = this.storageService.getUser();
    return user.roles.staff;
  }

  public isAdmin(): boolean {
    let user = this.storageService.getUser();
    return user.roles.admin;
  }
}
