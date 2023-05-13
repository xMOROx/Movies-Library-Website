import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {PaginationModel} from './models/pagination.model';
import {MoviesService} from 'src/app/features/services/movies.service';
import {take} from "rxjs";

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.scss']
})
export class ContentComponent implements OnInit {

  public contentType: string = '';
  public nowPlaying: Array<PaginationModel> = [];

  public totalResults: any;

  constructor(
    private moviesService: MoviesService,
    private router: Router
  ) {
    this.contentType = this.router.url.split('/')[1];
  }

  ngOnInit() {
    if (this.contentType === 'movies') {
      this.getNowPlayingMovies(1);
    } else {
      this.getNowPlayingTVShows(1);
    }
  }

  public getNowPlayingMovies(page: number) {
    this.moviesService.getNowPlayingMovies(page).pipe(take(1)).subscribe(
      {
        next: (response: any) => {
          this.nowPlaying = response.results;
          this.totalResults = response.total_results;
        },
        error: (_: any) => {
        }
      }
    );
  }

  public changePage(event: any) {
    if (this.contentType === 'movies') {
      this.getNowPlayingMovies(event.pageIndex + 1);
    } else {
      this.getNowPlayingTVShows(event.pageIndex + 1);
    }
  }

  private getNowPlayingTVShows(param: any) {
    //TODO: implement
  }
}
