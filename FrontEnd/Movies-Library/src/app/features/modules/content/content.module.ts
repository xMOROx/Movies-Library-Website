import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ContentComponent } from './content.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { DetailComponent } from './components/detail/detail.component';
import { FilterByStatusPipe } from './pipes/filter-by-status.pipe';
import { ContentRoutesModule } from './content.routes.module';
import { LatestMoviesComponent } from './components/movie-views/latest-movies/latest-movies.component';
import { PopularMoviesComponent } from './components/movie-views/popular-movies/popular-movies.component';
import { UpcomingMoviesComponent } from './components/movie-views/upcoming-movies/upcoming-movies.component';
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
    LatestMoviesComponent,
    PopularMoviesComponent,
    UpcomingMoviesComponent,
  ],
  declarations: [
    ContentComponent,
    DetailComponent,
    FilterByStatusPipe,
    LatestMoviesComponent,
    PopularMoviesComponent,
    UpcomingMoviesComponent,
  ]
})
export class ContentModule { }
