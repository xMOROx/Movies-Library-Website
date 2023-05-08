import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { PageNotFoundComponent } from './core/components/page-not-found/page-not-found.component';
import { LoginComponent } from 'src/app/authentication/components/login/login.component';
import { RegisterComponent } from './authentication/components/register/register.component';
import { ReactiveFormsModule } from "@angular/forms";
import { HttpClientModule, HTTP_INTERCEPTORS } from "@angular/common/http";
import { AuthInterceptor } from "./helpers/auth.interceptor";
import { ProfileComponent } from 'src/app/features/content/profile/profile.component';
import { MovieDetailsComponent } from 'src/app/features/content/movie-views/movie-details/movie-details.component';
import { PopularMoviesComponent } from 'src/app/features/content/movie-views/popular-movies/popular-movies.component';
import { LatestMoviesComponent } from 'src/app/features/content/movie-views/latest-movies/latest-movies.component';
import { UpcomingMoviesComponent } from 'src/app/features/content/movie-views/upcoming-movies/upcoming-movies.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { UserMoviesComponent } from 'src/app/features/content/movie-views/user-movies/user-movies.component';
import { FooterComponent } from './core/components/footer/footer.component';
import { NavBarComponent } from './core/components/nav-bar/nav-bar.component';
import { AggregatedMovieComponent } from 'src/app/features/content/movie-views/aggregated-movie/aggregated-movie.component';
import { FilterByStatusPipe } from './core/pipes/filter-by-status.pipe';
import { MaterialModule } from "./core/material/material.module";
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
    FilterByStatusPipe,
    FooterComponent,
    NavBarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MaterialModule,
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
