import { Injectable } from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "../../authentication/services/auth.service";
import {of} from "rxjs";

@Injectable()
export class AdminService {

    private endpoint: string = `${environment.backEnd}api/v1/admin/`;
    private language: string = "en-US";
    private region: string = "US";

    private httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        "Authorization": "Bearer " + localStorage.getItem('access_token')
      })
    };
    constructor(private http: HttpClient, private auth: AuthService) { }

    public getUsers(): any {
      if (!this.auth.isAuthenticated().subscribe((res: any) => res) && !this.auth.isAdmin()) {
        return of(null);
      }
      return this.http.get(this.endpoint + 'users', this.httpOptions);
    }

}
