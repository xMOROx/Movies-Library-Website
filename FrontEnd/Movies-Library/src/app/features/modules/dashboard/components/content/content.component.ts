import { Component, OnInit } from '@angular/core';
import {PaginationModel} from "../../../content/models/pagination.model";
import {MoviesService} from "../../../../services/movies.service";
import {Router} from "@angular/router";
import {StorageService} from "../../../../../authentication/services/storage.service";
import {AuthService} from "../../../../../authentication/services/auth.service";
import {TrashService} from "../../../../services/trash.service";

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.scss']
})
export class ContentComponent implements OnInit {
  public contentType: string = '';
  public content: Array<PaginationModel> = [];
  public totalResults: any;
  private userId: any;
  constructor(    private moviesService: MoviesService,
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

  public getMoviesForUser() {
    this.moviesService.getUserMovies(this.userId).subscribe(
      {
        next: (response: any) => {
          if (!response) {
            this.router.navigate(['/']);
          }
          this.content = response;
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
    this.trashService.getMoviesForUser(this.storage.getUser().id).subscribe(
      {
        next: (response: any) => {
          if (!response) {
            this.router.navigate(['/']);
          }
          this.content = response;
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

}
