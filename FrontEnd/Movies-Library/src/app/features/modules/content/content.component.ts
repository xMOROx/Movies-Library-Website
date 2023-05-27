import {Component, OnInit, ViewChild} from '@angular/core';
import {Router} from "@angular/router";
import {PaginationModel} from './models/pagination.model';
import {MoviesService} from 'src/app/features/services/movies.service';
import {take} from "rxjs";
import {MatPaginator} from "@angular/material/paginator";
import {FormControl} from "@angular/forms";
import {Genre} from "./models/Genre.model";
import {TvShowsService} from "../../services/tv-shows.service";

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
    private router: Router,
    private tvService: TvShowsService
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
      this.tvService.getGenres().pipe(take(1)).subscribe({
        next: ((response: any) => {
          this.categoryList = response.genres;
          this.categoryList?.forEach(category => {
            this.categoryDict[category.name] = category.id;
          });
        }),
        error: (_: any) => {

        }
      });
      this.getTvAiringToday(1);
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
      this.getTvAiringToday(event.pageIndex + 1);
    }
  }

  public applyFilter(filterValue: string) {
    this.query = '';
    this.categories.reset();
    this.filterType = filterValue;
    this.paginator?.firstPage();
    if (this.contentType === 'movies') {
      this.getMovies(1);
    } else {
      this.getTv(1);
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

  private getTv(page: number) {
    switch (this.filterType) {
      case 'Airing today':
        this.getTvAiringToday(page);
        break;
      case 'Airing this week':
        this.getTvAiringThisWeek(page);
        break;
      case 'Popular':
        this.getPopularTv(page);
        break;
      case 'Trending':
        this.getTrendingTv(page);
        break;
      case 'Upcoming':
        this.getUpcomingTv(page);
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

  private getTrendingMovies(page: any = 1, timeWindow: string = 'week') {
    this.moviesService.getTrendingMovies(page, timeWindow).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        }, error: (_: any) => {

        }
      });
  }

  private getTvAiringToday(page: any = 1) {
    this.tvService.getAiringToday(page).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        }, error: (_: any) => {

        }
      });
  }

  private getTvAiringThisWeek(page: any) {
    this.tvService.getAiringThisWeek(page).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        }, error: (_: any) => {

        }
      });
  }

  private getTrendingTv(page: any = 1, timeWindow: string = 'week') {
    this.tvService.getTrendingTv(page, timeWindow).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        }, error: (_: any) => {

        }
      });
  }

  private getPopularTv(page: any = 1) {
    this.tvService.getPopularTv(page).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        }, error: (_: any) => {

        }
      });
  }

  private getUpcomingTv(page: any = 1, timeWindow: string = 'week') {
    this.tvService.getUpcomingTv(page, timeWindow).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        }, error: (_: any) => {

        }
      });
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
    this.tvService.searchTv(query, page).pipe(take(1)).subscribe({
      next: (response: any) => {
        this.results = response.results;
        this.totalResults = response.total_results;
      }, error: (_: any) => {

      }
    });
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
    if (this.categories.value !== null) {
      let ids: string[] = [];
      let len = this.categories.value.length;

      for( let category of this.categories.value) {
        ids.push(this.categoryDict[category]);
      }

      this.tvService.getTvByGenreId(ids, page).pipe(take(1)).subscribe({
        next: (response) => {
          this.results = response.results;
          this.totalResults = response.total_results;
        },
        error: (_: any) => {

        }
      });
    }
  }


}
