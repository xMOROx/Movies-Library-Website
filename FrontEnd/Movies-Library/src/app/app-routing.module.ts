import { NgModule } from '@angular/core';
import { RouterModule, Routes } from "@angular/router";
import { AppComponent } from "./app.component";
import { LoginComponent } from "src/app/authentication/components/login/login.component";
import { RegisterComponent } from "src/app/authentication/components/register/register.component";
import { PageNotFoundComponent } from "src/app/core/components/page-not-found/page-not-found.component";
import { ProfileComponent } from 'src/app/features/content/profile/profile.component';
import { MovieDetailsComponent } from "src/app/features/content/movie-views/movie-details/movie-details.component";
import { UserMoviesComponent } from "src/app/features/content/movie-views/user-movies/user-movies.component";


const routes: Routes = [
  { path: 'home', component: AppComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'user-profile/:id', component: ProfileComponent },
  { path: 'user-profile/:id/movies', component: UserMoviesComponent },
  { path: 'movies/:id', component: MovieDetailsComponent },
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
