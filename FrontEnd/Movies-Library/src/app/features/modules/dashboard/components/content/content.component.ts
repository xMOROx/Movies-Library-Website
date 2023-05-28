import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {PaginationModel} from "../../../content/models/pagination.model";
import {MoviesService} from "../../../../services/movies.service";
import {Router} from "@angular/router";
import {StorageService} from "../../../../../authentication/services/storage.service";
import {AuthService} from "../../../../../authentication/services/auth.service";
import {TrashService} from "../../../../services/trash.service";
import {filter} from "rxjs/operators";
import {TvShowsService} from "../../../../services/tv-shows.service";

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.scss']
})
export class ContentComponent implements OnInit {
  public contentType: string = "";
  public content: Array<PaginationModel> = [];
  public totalResults: any;
  public filterType: string = 'all';
  private userId: any;

  constructor(private moviesService: MoviesService,
              private storage: StorageService,
              private auth: AuthService,
              private trashService: TrashService,
              private tvService: TvShowsService,
              private router: Router) {
    this.contentType = this.router.url.split('/')[2];
  }

  ngOnInit() {
    this.userId = this.storage.getUser().id;

    if (this.contentType === 'movies') {
      this.getMoviesForUser();
    } else if (this.contentType === 'trash') {
      this.getMoviesFromTrash();
    } else if (this.contentType === "tv-shows") {
      this.getTVShowsForUser();
    }
  }

  public getMoviesForUser(filter: string = "all") {
    this.moviesService.getUserMovies(this.userId, false).subscribe(
      {
        next: (response: any) => {
          if (!response) {
            this.router.navigate(['/']);
          }
          this.content = response.results;
          this.totalResults = response.count;
          this.content = this.filterContentByType(this.content, filter);
          // console.log(this.content)
        },
        error: (_: any) => {
        }
      }
    );
  }

  public getTVShowsForUser(filter: string = "all") {
    this.tvService.getUserTvShows(this.userId, false).subscribe(
      {
        next: (response: any) => {
          if (!response) {
            this.router.navigate(['/']);
          }
          this.content = response.results;
          this.totalResults = response.count;
          this.content = this.filterContentByType(this.content, filter);
        },
        error: (_: any) => {
        }
      }
    );
  }

  public getMoviesFromTrash() {
    this.trashService.getTrashForUser(this.storage.getUser().id, "movies").subscribe(
      {
        next: (response: any) => {
          if (!response) {
            this.router.navigate(['/']);
          }
          this.content = response.results;
          this.totalResults = response.count;
        },
        error: (_: any) => {
        }
      }
    );
  }

  public changePage(event: any) {
    if (this.contentType === 'movies') {
      this.getMoviesForUser();
    } else if (this.contentType === 'trash') {
      this.getMoviesFromTrash();
    } else if (this.contentType === "TV-shows") {
      this.getTVShowsForUser();
    }
  }

  private filterContentByType(content: Array<PaginationModel>, filter: string) {
    if (filter.toLowerCase() === 'all') {
      this.totalResults = content.length;
      return content;
    }
    if (filter.toLowerCase() === 'favorite') {
      let filteredContent = content.filter((content: any) => content.is_favorite);
      this.totalResults = filteredContent.length;
      return filteredContent;
    } else {
      let filteredContent = content.filter((content: any) => content.status.toLowerCase() === filter.toLowerCase());
      this.totalResults = filteredContent.length;
      return filteredContent;
    }
  }

  public applyFilter(filter: string) {
    this.filterType = filter;
    if (this.contentType.toLowerCase() === 'movies') {
      this.getMoviesForUser(this.filterType);
    } else if (this.contentType.toLowerCase() === 'trash') {
      this.getMoviesFromTrash();
    } else if (this.contentType.toLowerCase() === "tv-shows".toLowerCase()) {
      this.getTVShowsForUser(this.filterType);
    }
  }

}
