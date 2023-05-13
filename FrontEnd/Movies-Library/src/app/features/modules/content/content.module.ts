import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ContentComponent } from './content.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { DetailComponent } from './components/detail/detail.component';
import { FilterByStatusPipe } from './pipes/filter-by-status.pipe';
import { AggregatedMovieComponent } from './components/movie-views/aggregated-movie/aggregated-movie.component';
import { ContentRoutesModule } from './content.routes.module';
import { LatestMoviesComponent } from './components/movie-views/latest-movies/latest-movies.component';
import { PopularMoviesComponent } from './components/movie-views/popular-movies/popular-movies.component';
import { UpcomingMoviesComponent } from './components/movie-views/upcoming-movies/upcoming-movies.component';
import { MovieDetailsForUserComponent } from './components/movie-views/movie-details-for-user/movie-details-for-user.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    ContentRoutesModule,
    HttpClientModule
  ],
  exports: [
    ContentComponent,
    DetailComponent,
    FilterByStatusPipe,
    AggregatedMovieComponent,
    LatestMoviesComponent,
    PopularMoviesComponent,
    UpcomingMoviesComponent,
    MovieDetailsForUserComponent
  ],
  declarations: [
    ContentComponent,
    DetailComponent,
    FilterByStatusPipe,
    AggregatedMovieComponent,
    LatestMoviesComponent,
    PopularMoviesComponent,
    UpcomingMoviesComponent,
    MovieDetailsForUserComponent
  ]
})
export class ContentModule { }
