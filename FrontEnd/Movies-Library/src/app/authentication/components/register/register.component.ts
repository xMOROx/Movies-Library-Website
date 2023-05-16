import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/authentication/services/auth.service';
import { ValidateService } from "src/app/core/services/validate.service";
import { MatDialogRef } from '@angular/material/dialog';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  public signupForm: FormGroup;

  constructor(public fb: FormBuilder,
    public authService: AuthService,
    public router: Router,
    private validateService: ValidateService,
    public dialogRef: MatDialogRef<RegisterComponent>
  ) {
    this.signupForm = this.fb.group({
      email: [''],
      password: [''],
      last_name: [''],
      first_name: ['']
    })
  }


  ngOnInit(): void { }

  public registerUser(): void {
    if(!this.validateService.validatePassword(this.signupForm.value.password)) {
      this.signupForm.controls['password'].setErrors({ 'incorrect': true });
      return;
    }

    if (!this.validateService.validateEmail(this.signupForm.value.email)) {
      this.signupForm.controls['email'].setErrors({ 'incorrect': true });
      return;
    }

    this.authService.singUp(this.signupForm.value)
      .subscribe(
        {
          next: (res) => {
            if (res.status == 201) {
              this.signupForm.reset();
              this.router.navigate(['/']);
              this.dialogRef.close();
            }
          },
          error: (err) => {
            this.handleError(err);
          }
        }

      );
  }

  public handleError(error: HttpErrorResponse): any {
    if (error.status === 409) {
      this.signupForm.controls['email'].setErrors({ 'conflict': true });
    }
  }

}
