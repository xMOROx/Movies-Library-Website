import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UsersComponent } from './users.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { ProfileComponent } from './components/profile/profile.component';
import { UserMoviesComponent } from './components/user-movies/user-movies.component';
import { ContentModule } from '../content/content.module';
import { UsersRoutesModule } from './users.routes.module';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    ContentModule,
    UsersRoutesModule,
    HttpClientModule
  ],
  exports: [UsersComponent, ProfileComponent, UserMoviesComponent],
  declarations: [UsersComponent, ProfileComponent, UserMoviesComponent]
})
export class UsersModule { }
