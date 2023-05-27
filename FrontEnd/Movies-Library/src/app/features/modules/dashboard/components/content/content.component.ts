import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {PaginationModel} from "../../../content/models/pagination.model";
import {MoviesService} from "../../../../services/movies.service";
import {Router} from "@angular/router";
import {StorageService} from "../../../../../authentication/services/storage.service";
import {AuthService} from "../../../../../authentication/services/auth.service";
import {TrashService} from "../../../../services/trash.service";
import {filter} from "rxjs/operators";

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
              private router: Router) {
    this.contentType = this.router.url.split('/')[2];
  }

  ngOnInit() {
    this.userId = this.storage.getUser().id;

    if (this.contentType === 'movies') {
      this.getMoviesForUser();
    } else if (this.contentType === 'trash') {
      this.getMoviesFromTrash();
    } else if (this.contentType === "TV-shows") {
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
          //TODO: total results
          this.totalResults = response.count;
          this.content = this.filterMoviesByType(this.content, filter);
          // console.log(this.content)
        },
        error: (_: any) => {
        }
      }
    );
  }

  public getTVShowsForUser() {
    //TODO: implement
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

  private filterMoviesByType(movies: Array<PaginationModel>, filter: string) {
    if (filter.toLowerCase() === 'all') {
      this.totalResults = movies.length;
      return movies;
    }
    if (filter.toLowerCase() === 'favorite') {
      let filteredMovies = movies.filter((movie: any) => movie.is_favorite);
      this.totalResults = filteredMovies.length;
      return filteredMovies;
    } else {
      let filteredMovies = movies.filter((movie: any) => movie.status.toLowerCase() === filter.toLowerCase());
      this.totalResults = filteredMovies.length;
      return filteredMovies;
    }
  }

  public applyFilter(filter: string) {
    this.filterType = filter;
    if (this.contentType.toLowerCase() === 'movies') {
      this.getMoviesForUser(this.filterType);
    } else if (this.contentType.toLowerCase() === 'trash') {
      this.getMoviesFromTrash();
    } else if (this.contentType.toLowerCase() === "TV-shows".toLowerCase()) {
      this.getTVShowsForUser();
    }
  }

}
