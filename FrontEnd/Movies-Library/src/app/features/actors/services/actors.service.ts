import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ActorsService {
  private base_url = `${environment.backEnd}${environment.api}/${environment.api_version}/actors`;
  constructor(private httpClient: HttpClient) { }

  public getActorDetails(id: number): Observable<any> {
    return this.httpClient.get(`${this.base_url}/${id}`);
  }

  public getActorExternalData(id: number): Observable<any> {
    return this.httpClient.get(`${this.base_url}/${id}/external_data`);
  }

  public getActorCast(id: number): Observable<any> {
    return this.httpClient.get(`${this.base_url}/${id}/cast`);
  }
}
