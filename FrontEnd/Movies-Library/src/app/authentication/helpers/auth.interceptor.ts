import { Injectable } from "@angular/core";
import { HttpInterceptor, HttpRequest, HttpHandler, HttpErrorResponse } from "@angular/common/http";
import { AuthService } from "src/app/authentication/services/auth.service";
import { catchError, filter, switchMap, take } from "rxjs/operators";
import { BehaviorSubject, throwError } from "rxjs";
import { TokenService } from "src/app/authentication/services/token.service";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private isRefreshing = false;
  private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

  constructor(private authService: AuthService, private tokenService: TokenService) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    const authToken = this.tokenService.getAccessToken();
    if (authToken) {
      this.addTokenHeader(req, authToken);
    }
    return next.handle(req).pipe(catchError(error => {
      if (error instanceof HttpErrorResponse && !req.url.includes('auth/signin') && error.status === 401) {
        return this.handle401Error(req, next);
      }
      return throwError(() => error);
    }));
  }

  private handle401Error(request: HttpRequest<any>, next: HttpHandler) {
    if (!this.isRefreshing) {
      this.isRefreshing = true;
      this.refreshTokenSubject.next(null);
      const refreshToken = this.tokenService.getRefreshToken();
      if (refreshToken) {
        return this.authService.refreshToken(refreshToken).pipe(
          switchMap((token: any) => {
            this.isRefreshing = false;
            this.tokenService.saveToken(token.access);
            this.tokenService.saveRefreshToken(token.refresh);
            this.refreshTokenSubject.next(token.access);

            return next.handle(this.addTokenHeader(request, token.access));
          }), catchError((error) => {
            this.isRefreshing = false;
            this.authService.logout();
            return throwError(() => error);
          }));
      }
    }
    return this.refreshTokenSubject.pipe(
      filter(token => token !== null),
      take(1),
      switchMap((token) => next.handle(this.addTokenHeader(request, token)))
    );
  }

  private addTokenHeader(request: HttpRequest<any>, token: string) {
    return request.clone({ headers: request.headers.set("Authorization", "Bearer " + token) });
  }
}
