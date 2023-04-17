import { Injectable } from '@angular/core';
import jwt_decode from "jwt-decode";

@Injectable({
  providedIn: 'root'
})
export class TokenService {

  constructor() { }

  public getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  public saveToken(token: string): void {
    localStorage.removeItem('access_token');
    localStorage.setItem('access_token', token);
  }

  public getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token')
  }

  public saveRefreshToken(token: string): void {
    localStorage.removeItem('refresh_token');
    localStorage.setItem('refresh_token', token);
  }

  public getDecodedAccessToken(token: string): any {
    try {
      return jwt_decode(token);
    } catch (Error) {
      return null;
    }
  }
}
