import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { User } from "src/app/authentication/models/User";
import { environment } from "src/environments/environment";
import { FormBuilder, FormGroup } from '@angular/forms';
import { AuthService } from 'src/app/authentication/services/auth.service';
import { Router } from '@angular/router';
import { ValidateService } from "src/app/core/services/validate.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  signInForm: FormGroup;
  constructor(
    public fb: FormBuilder,
    public authService: AuthService,
    public router: Router,
    private validateService: ValidateService
  ) {
    this.signInForm = this.fb.group({
      email: [''],
      password: [''],
    });
  }

  ngOnInit(): void { }
  public signIn(): void {
    if (this.validateService.validateEmail(this.signInForm.value.email)) {
      this.authService.signIn(this.signInForm.value);
    }
  }
}
