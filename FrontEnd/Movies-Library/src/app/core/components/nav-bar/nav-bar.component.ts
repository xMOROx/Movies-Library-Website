import { Component, HostListener, OnInit } from '@angular/core';
import { MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { LoginComponent } from 'src/app/authentication/components/login/login.component';
import { RegisterComponent } from 'src/app/authentication/components/register/register.component';
import { AuthService } from 'src/app/authentication/services/auth.service';
import {User} from "../../../authentication/models/User";
import {StorageService} from "../../../authentication/services/storage.service";
@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.scss']
})
export class NavBarComponent implements OnInit {
  public isScrolled: boolean = false;
  public dialogSignIn!: MatDialogRef<LoginComponent>;
  public dialogRegister!: MatDialogRef<RegisterComponent>;
  public user?: User;
  public isAuth: boolean = false;

  @HostListener('window:scroll')
  scrollEvent() {
    this.isScrolled = window.scrollY >= 30;
  }
  constructor(public dialog: MatDialog,
              public authService: AuthService,
              private storage: StorageService,) { }

  ngOnInit() {
    this.user = this.storage.getUser();
    this.authService.isAuthenticated().subscribe((isAuth: boolean) => {
      this.isAuth = isAuth;
    });
  }

  public openSignDialog() {
    this.dialogSignIn = this.dialog.open(LoginComponent, {
      minWidth: '400px',
      width: '30vw',
      maxWidth: '600px',
      height: 'auto',
      data: {
      },
      backdropClass: 'backdropBackground'

    });
  }

  public openRegisterDialog() {
    this.dialogRegister = this.dialog.open(RegisterComponent, {
      width: '30vw',
      minWidth: '400px',
      maxWidth: '600px',
      minHeight: '550px',
      height: 'auto',
      data: {
      },
      backdropClass: 'backdropBackground'
    });
  }

  public signOut() {
    this.authService.logout();
  }

}
