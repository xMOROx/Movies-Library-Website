import {Component, OnInit,} from '@angular/core';
import SwiperCore, {Pagination, SwiperOptions,} from 'swiper';
import {MovieModel} from 'src/app/features/modules/content/models/Movie.model';
import {TvModel} from 'src/app/features/modules/content/models/Tv.model';
import {MoviesService} from "src/app/features/services/movies.service";
import {ActorModel} from '../modules/actors/models/Actor.model';
import {ActorsService} from '../modules/actors/services/actors.service';
import {TvShowsService} from "../services/tv-shows.service";

SwiperCore.use([Pagination]);

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
    pagination: {clickable: true,},
    scrollbar: {draggable: true},
    breakpoints: {
      992: {slidesPerView: 6.3, spaceBetween: 20, slidesOffsetBefore: 0, slidesOffsetAfter: 0},
      768: {slidesPerView: 4.3, spaceBetween: 15, slidesOffsetBefore: 0, slidesOffsetAfter: 0},
      576: {slidesPerView: 3.3, spaceBetween: 15, slidesOffsetBefore: 0, slidesOffsetAfter: 0},
      320: {slidesPerView: 2.3, spaceBetween: 10, slidesOffsetBefore: 10, slidesOffsetAfter: 10},
    }
  };

  public movieTabList = ['Now playing', 'Upcoming week', "Upcoming month", 'Popular', "Trending day", "Trending week"];
  public moviesList: Array<MovieModel> = [];
  public selectedMovieTab = 0;

  public tvShowsTabList = ['Airing today', 'Airing this week', 'Popular', 'Trending', 'Upcoming'];
  public tvShowsList: Array<TvModel> = [];
  public selectedTVTab = 0;

  public actorsTabList = ['Trending day', 'Trending week'];
  public actorsList: Array<ActorModel> = [];
  public selectedActorTab = 0;
  public sortActorBy: string = 'popularity';
  public sortActorOrder: string = 'desc';


  constructor(private moviesService: MoviesService, private actorsService: ActorsService, private tvService: TvShowsService) {
  }

  ngOnInit() {
    this.getMovies(this.movieTabList[this.selectedMovieTab]);
    this.getTv(this.tvShowsTabList[this.selectedTVTab]);
    this.getActors(this.actorsTabList[this.selectedActorTab]);
  }

  private getTrendingMovies(page: number = 1, timeWindow: string = 'week') {
    this.moviesService.getTrendingMovies(page, timeWindow).subscribe((movies) => {
      this.moviesList = movies?.results;
    });
  }

  private getTrendingTv(page: number = 1, timeWindow: string = 'week') {
    this.tvService.getTrendingTv(page, timeWindow).subscribe((tv) => {
      this.tvShowsList = tv?.results;
    });
  }

  private getUpcomingMovies(page: number = 1, timeWindow: string = 'week') {
    this.moviesService.getUpcomingMovies(page, timeWindow).subscribe((movies) => {
      this.moviesList = movies?.results;
    });
  }

  private getUpcomingTv(page: number = 1, timeWindow: string = 'week') {
    this.tvService.getUpcomingTv(page, timeWindow).subscribe((tv) => {
      this.tvShowsList = tv?.results;
    });
  }

  private getNowPlayingMovies(page: number = 1) {
    this.moviesService.getNowPlayingMovies(page).subscribe((movies) => {
      this.moviesList = movies?.results;
    });
  }

  private getAiringToday(page: number = 1) {
    this.tvService.getAiringToday(page).subscribe((tv) => {
      this.tvShowsList = tv?.results;
    });
  }

  private getAiringThisWeek(page: number = 1) {
    this.tvService.getAiringThisWeek(page).subscribe((tv) => {
      this.tvShowsList = tv?.results;
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

  private getPopularTv(page: number = 1) {
    this.tvService.getPopularTv(page).subscribe((tv) => {
      this.tvShowsList = tv?.results;
    });
  }

  private getTrendingActors(page: number = 1, timeWindow: string = 'week') {
    this.actorsService.getTrendingActors(page, timeWindow).subscribe((actors) => {
      this.actorsList = actors?.results;
    });
  }

  private getMovies(tabName: string) {
    if (tabName === 'Trending week') {
      this.getTrendingMovies(1, "week");
    } else if (tabName === 'Trending day') {
      this.getTrendingMovies(1, "day");
    } else if (tabName === 'Upcoming week') {
      this.getUpcomingMovies(1, "week");
    } else if (tabName === 'Upcoming month') {
      this.getUpcomingMovies(1, "month");
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

  private getTv(tabName: string) {
    if (tabName === 'Airing today') {
      this.getAiringToday();
    } else if (tabName === 'Airing this week') {
      this.getAiringThisWeek();
    } else if (tabName === 'Trending') {
      this.getTrendingTv();
    } else if (tabName === 'Upcoming') {
      this.getUpcomingTv();
    } else if (tabName === 'Popular') {
      this.getPopularTv();
    }
  }

  public tabMovieChange(event: any) {
    this.selectedMovieTab = event.index;
    this.getMovies(this.movieTabList[this.selectedMovieTab]);
  }


  public tabTVChange(event: any) {
    this.selectedTVTab = event.index;
    this.getTv(this.tvShowsTabList[this.selectedTVTab]);
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
