import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UsersComponent } from './users.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { ProfileComponent } from './components/profile/profile.component';
import { ContentModule } from '../content/content.module';
import { UsersRoutesModule } from './users.routes.module';
import { HttpClientModule } from '@angular/common/http';
import { EditProfileComponent } from "./components/edit-profile/edit-profile.component";
import { ReactiveFormsModule } from "@angular/forms";
import { ChangePasswordComponent } from './components/ChangePassword/ChangePassword.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    UsersRoutesModule,
    HttpClientModule,
    ContentModule,
    ReactiveFormsModule,

  ],
  exports: [UsersComponent, ProfileComponent],
  declarations: [UsersComponent, ProfileComponent, EditProfileComponent, ChangePasswordComponent]
})
export class UsersModule { }
