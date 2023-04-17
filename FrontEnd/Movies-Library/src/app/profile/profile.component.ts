import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { User } from '../models/User';
import { AuthService } from '../services/auth.service';
import { StorageService } from '../services/storage.service';

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
    private storageService: StorageService
  ) {
    this.currentUser = this.storageService.getUser();

  }

  ngOnInit() {
  }

}
