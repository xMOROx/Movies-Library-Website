import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  public signupForm: FormGroup;

  constructor(public fb: FormBuilder,
    public authService: AuthService,
    public router: Router) {
    this.signupForm = this.fb.group({
      email: [''],
      password: [''],
      lastName: [''],
      firstName: ['']
    })
  }


  ngOnInit(): void { }

  registerUser() {
    this.authService.singUp(this.signupForm.value).subscribe((res) => {
      if (res.result) {
        this.signupForm.reset();
        this.router.navigate(['login']);
      }
    })
  }

}
