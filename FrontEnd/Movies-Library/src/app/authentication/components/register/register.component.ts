import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/authentication/services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  public signupForm: FormGroup;

  constructor(public fb: FormBuilder,
    public authService: AuthService,
    public router: Router) {
    this.signupForm = this.fb.group({
      email: [''],
      password: [''],
      last_name: [''],
      first_name: ['']
    })
  }


  ngOnInit(): void { }

  registerUser() {
    this.authService.singUp(this.signupForm.value).subscribe((res) => {
      if (res.status == 201) {
        this.signupForm.reset();
        this.router.navigate(['login']);
      }
    });
  }

}
