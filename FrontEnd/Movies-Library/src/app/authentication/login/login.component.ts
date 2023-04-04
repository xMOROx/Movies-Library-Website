import { Component } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {User} from "../../models/User";
import {environment} from "../../../environments/environment";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  public email: string;
  public password: string;

  constructor(private httpClient: HttpClient) {
    this.email = "";
    this.password = "";
  }

  onSubmit() {
    let credentials: User = {
      email: this.email,
      password: this.password
    };
    this.httpClient.post(environment.backEnd + '/auth/login', credentials).subscribe(r => {
      this.httpClient.get(environment.backEnd + '/auth/me').subscribe(r => {
        console.log(r);
      });
    });
  }

}
