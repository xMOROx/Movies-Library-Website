import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { User } from '../models/User';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  public currentUser: User = {
    email: '',
    first_name: '',
    last_name: '',
    password: '',
  };
  constructor(
    public authService: AuthService,
    private actRoute: ActivatedRoute
  ) {
    let id: any = this.actRoute.snapshot.paramMap.get('id');
    this.authService.getUserProfile(id).subscribe((res) => {
      this.currentUser = res;
    });
  }

  ngOnInit() {
  }

}
