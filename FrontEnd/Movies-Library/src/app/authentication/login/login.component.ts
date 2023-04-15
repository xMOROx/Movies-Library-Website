import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { User } from "../../models/User";
import { environment } from "../../../environments/environment";
import { FormBuilder, FormGroup } from '@angular/forms';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  signinForm: FormGroup;
  constructor(
    public fb: FormBuilder,
    public authService: AuthService,
    public router: Router
  ) {
    this.signinForm = this.fb.group({
      email: [''],
      password: [''],
    });
  }

  ngOnInit(): void { }
  public signIn(): void {
    this.authService.signIn(this.signinForm.value);
  }
} 
