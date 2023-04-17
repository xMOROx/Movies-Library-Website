import { NgModule } from '@angular/core';
import { RouterModule, Routes } from "@angular/router";
import { AppComponent } from "./app.component";
import { LoginComponent } from "./authentication/login/login.component";
import { RegisterComponent } from "./authentication/register/register.component";
import { PageNotFoundComponent } from "./page-not-found/page-not-found.component";
import { ProfileComponent } from './profile/profile.component';
import {MovieDetailsComponent} from "./movie-views/movie-details/movie-details.component";


const routes: Routes = [
  { path: 'home', component: AppComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'user-profile/:id', component: ProfileComponent },
  { path: 'movies/:id', component: MovieDetailsComponent },
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
