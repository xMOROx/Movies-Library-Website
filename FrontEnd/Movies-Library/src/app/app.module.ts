import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppComponent} from './app.component';
import {AppRoutingModule} from './app-routing.module';
import {PageNotFoundComponent} from './page-not-found/page-not-found.component';
import {LoginComponent} from './authentication/login/login.component';
import {RegisterComponent} from './authentication/register/register.component';
import {ReactiveFormsModule} from "@angular/forms";
import {HttpClientModule, HTTP_INTERCEPTORS} from "@angular/common/http";
import {AuthInterceptor} from "./helpers/auth.interceptor";
import {ProfileComponent} from './profile/profile.component';
import {MovieDetailsComponent} from './movie-views/movie-details/movie-details.component';
import {PopularMoviesComponent} from './movie-views/popular-movies/popular-movies.component';
import {LatestMoviesComponent} from './movie-views/latest-movies/latest-movies.component';
import {UpcomingMoviesComponent} from './movie-views/upcoming-movies/upcoming-movies.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";
import { UserMoviesComponent } from './movie-views/user-movies/user-movies.component';
import { AggregatedMovieComponent } from './movie-views/aggregated-movie/aggregated-movie.component';
import { FilterByStatusPipe } from './pipes/filter-by-status.pipe';

@NgModule({
  declarations: [
    AppComponent,
    PageNotFoundComponent,
    LoginComponent,
    RegisterComponent,
    ProfileComponent,
    MovieDetailsComponent,
    PopularMoviesComponent,
    LatestMoviesComponent,
    UpcomingMoviesComponent,
    UserMoviesComponent,
    AggregatedMovieComponent,
    FilterByStatusPipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatFormFieldModule,
    MatSelectModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
