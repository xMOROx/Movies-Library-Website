import { Component, OnInit } from '@angular/core';
import SwiperCore, { Pagination, SwiperOptions } from 'swiper';
import { MovieModel } from 'src/app/features/modules/content/models/Movie.model';
import { TvModel } from 'src/app/features/modules/content/models/Tv.model';
import { MoviesService } from "src/app/features/services/movies.service";
import { ActorModel } from '../modules/actors/models/Actor.model';
import { ActorsService } from '../modules/actors/services/actors.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  public config: SwiperOptions = {
    slidesPerView: 2.3,
    spaceBetween: 20,
    navigation: true,
    watchSlidesProgress: true,
    grabCursor: true,
    pagination: { clickable: true },
    scrollbar: { draggable: true },
    breakpoints: {
      992: { slidesPerView: 6.3, spaceBetween: 20, slidesOffsetBefore: 0, slidesOffsetAfter: 0 },
      768: { slidesPerView: 4.3, spaceBetween: 15, slidesOffsetBefore: 0, slidesOffsetAfter: 0 },
      576: { slidesPerView: 3.3, spaceBetween: 15, slidesOffsetBefore: 0, slidesOffsetAfter: 0 },
      320: { slidesPerView: 2.3, spaceBetween: 10, slidesOffsetBefore: 10, slidesOffsetAfter: 10 },
    }
  };

  public movieTabList = ['Now playing', 'Upcoming', 'Popular', "Latest", "Trending"];
  public moviesList: Array<MovieModel> = [];
  public selectedMovieTab = 0;

  public tvShowsTabList = ['Airing Today', 'Currently Airing', 'Popular'];
  public tvShowsList: Array<TvModel> = [];
  public selectedTVTab = 0;

  public actorsTabList = ['Trending day', 'Trending week'];
  public actorsList: Array<ActorModel> = [];
  public selectedActorTab = 0;
  public sortActorBy: string = 'popularity';
  public sortActorOrder: string = 'desc';


  constructor(private moviesService: MoviesService, private actorsService: ActorsService) { }

  ngOnInit() {
    this.getMovies(this.movieTabList[this.selectedMovieTab]);
    this.getActors(this.actorsTabList[this.selectedActorTab]);
  }

  private getTrendingMovies(page: number = 1, mediaType: string = 'movie', timeWindow: string = 'week') {
    this.moviesService.getTrendingMovies(page, mediaType, timeWindow).subscribe((movies) => {
      this.moviesList = movies?.results;
    });
  }

  private getUpcomingMovies(page: number = 1, timeWindow: string = 'week') {
    this.moviesService.getUpcomingMovies(page, timeWindow).subscribe((movies) => {
      this.moviesList = movies?.results;
    });
  }

  private getNowPlayingMovies(page: number = 1) {
    this.moviesService.getNowPlayingMovies(page).subscribe((movies) => {
      this.moviesList = movies?.results;
    });
  }

  private getLatestMovies(page: number = 1) {
    this.moviesService.getLatestMovies(page).subscribe((movies) => {
      this.moviesList = movies?.results;
    });
  }

  private getPopularMovies(page: number = 1) {
    this.moviesService.getPopularMovies(page).subscribe((movies) => {
      this.moviesList = movies?.results;
    });
  }

  private getTrendingActors(page: number = 1, timeWindow: string = 'week') {
    this.actorsService.getTrendingActors(page, timeWindow).subscribe((actors) => {
      this.actorsList = actors?.results;
    });
  }

  private getMovies(tabName: string) {
    //TODO: improve if else => dictionary
    if (tabName === 'Trending') {
      this.getTrendingMovies(); //TODO: Add time window
    } else if (tabName === 'Upcoming') {
      this.getUpcomingMovies(); //TODO: Add time window
    } else if (tabName === 'Now playing') {
      this.getNowPlayingMovies();
    } else if (tabName === 'Latest') {
      this.getLatestMovies();
    } else if (tabName === 'Popular') {
      this.getPopularMovies();
    }
  }

  private getActors(tabName: string) {
    if (tabName === 'Trending day') {
      this.getTrendingActors(1, "day");
    } else if (tabName === 'Trending week') {
      this.getTrendingActors(1, "week");
    }
  }

  public tabMovieChange(event: any) {
    this.selectedMovieTab = event.index;
    this.getMovies(this.movieTabList[this.selectedMovieTab]);
  }


  public tabTVChange(event: any) {
    this.selectedTVTab = event.index;
  }

  public tabActorChange(event: any) {
    this.selectedActorTab = event.index;
    this.getActors(this.actorsTabList[this.selectedActorTab]);
  }

  public actorSortingChange(sortBy: string, sortOrder: string) {
    this.sortActorBy = sortBy;
    this.sortActorOrder = sortOrder;
  }

}
