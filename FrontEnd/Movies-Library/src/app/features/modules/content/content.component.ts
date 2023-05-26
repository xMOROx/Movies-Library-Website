import {Component, OnInit, ViewChild} from '@angular/core';
import {Router} from "@angular/router";
import {PaginationModel} from './models/pagination.model';
import {MoviesService} from 'src/app/features/services/movies.service';
import {take} from "rxjs";
import {MatPaginator} from "@angular/material/paginator";
import {FormControl} from "@angular/forms";
import {Genre} from "./models/Genre.model";

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.scss']
})
export class ContentComponent implements OnInit {

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  public contentType: string = '';
  public results: Array<PaginationModel> = [];
  public filterType: string = 'Now Playing';
  public totalResults: any;
  public query: string = '';

  categories = new FormControl('');
  categoryList?: Array<Genre>;
  private categoryDict: {[name: string]: string;} = {};

  constructor(
    private moviesService: MoviesService,
    private router: Router
  ) {
    this.contentType = this.router.url.split('/')[1];
  }

  ngOnInit() {
    if (this.contentType === 'movies') {
      this.moviesService.getGenres().pipe(take(1)).subscribe({
        next: ((response: any) => {
          this.categoryList = response.genres;
          this.categoryList?.forEach(category => {
            this.categoryDict[category.name] = category.id;
          });
      }),
        error: (_: any) => {

        }
      });
      this.getMovies(1)
    } else {
      this.getNowPlayingTVShows(1);
    }
  }

  public searchByQuery() {
    if (this.query !== '') {
      this.categories.reset();
      this.filterType = 'Search';
      this.paginator?.firstPage();
      if (this.contentType === 'movies') {
        this.searchMovies(this.query);
      } else {
        this.searchTVShows(this.query);
      }
    }
  }

  public searchByCategories(event: any) {
    event.stopPropagation();
    if(this.categories.value !== '') {
      this.query = '';
      this.filterType = 'Search by categories';
      this.paginator?.firstPage();
      if (this.contentType === 'movies') {
        this.searchMoviesByCategories();
      } else {
        this.searchTVShowsByCategories();
      }
    }
  }

  public changePage(event: any) {
    if (this.contentType === 'movies') {
      this.getMovies(event.pageIndex + 1);
    } else {
      this.getNowPlayingTVShows(event.pageIndex + 1);
    }
  }

  public applyFilter(filterValue: string) {
    this.query = '';
    this.categories.reset();
    this.filterType = filterValue;
    this.paginator?.firstPage();
    if (this.contentType === 'movies') {
      this.getMovies(1);
    }
  }

  private getMovies(page: number) {
    switch (this.filterType) {
      case 'Now Playing':
        this.getNowPlayingMovies(page);
        break;
      case 'Upcoming':
        this.getUpcomingMovies(page);
        break;
      case 'Popular':
        this.getPopularMovies(page);
        break;
      case 'Trending':
        this.getTrendingMovies(page);
        break;
      case 'Search':
        this.searchMovies(this.query, page);
        break;
      case 'Search by categories':
        this.searchMoviesByCategories(page);
        break;
    }
  }

  private getNowPlayingMovies(page: number = 1) {
    this.moviesService.getNowPlayingMovies(page).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        },
        error: (_: any) => {
        }
      }
    );
  }

  private getUpcomingMovies(page: any = 1, timeWindow: string = 'week') {
    this.moviesService.getUpcomingMovies(page, timeWindow).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        }, error: (_: any) => {

        }
      });
  }

  private getPopularMovies(page: any = 1) {
    this.moviesService.getPopularMovies(page).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        }, error: (_: any) => {

        }
      });
  }

  private getTrendingMovies(page: any = 1, mediaType: string = 'movie', timeWindow: string = 'week') {
    this.moviesService.getTrendingMovies(page, mediaType, timeWindow).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        }, error: (_: any) => {

        }
      });
  }

  private getNowPlayingTVShows(param: any) {
    //TODO: implement
  }

  private searchMovies(query: string, page: any = 1) {
    this.moviesService.searchMovies(query, page).pipe(take(1)).subscribe({
      next: (response: any) => {
        this.results = response.results;
        this.totalResults = response.total_results;
      }, error: (_: any) => {

      }
    });
  }

  private searchTVShows(query: string, page: any = 1) {
    // TODO: implement
  }

  private searchMoviesByCategories(page: any = 1) {
    if (this.categories.value !== null) {
      let ids: string[] = [];
      let len = this.categories.value.length;

      for( let category of this.categories.value) {
        ids.push(this.categoryDict[category]);
      }

      this.moviesService.getMoviesByGenreId(ids, page).pipe(take(1)).subscribe({
        next: (response) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        },
        error: (_: any) => {

        }
      });
    }
  }

  private searchTVShowsByCategories(page: any = 1) {
    // TODO: implement
  }


}
