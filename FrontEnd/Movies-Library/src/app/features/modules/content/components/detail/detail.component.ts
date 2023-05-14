
import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import {take, throwError} from 'rxjs';
import { MoviesService } from 'src/app/features/services/movies.service';
import { ContentModel } from '../../models/Content.model';
import { MovieModel } from '../../models/Movie.model';
import { PaginationModel } from '../../models/pagination.model';
import { TvModel } from '../../models/Tv.model';
import {User} from "../../../../../authentication/models/User";
import {StorageService} from "../../../../../authentication/services/storage.service";
import {catchError} from "rxjs/operators";
import {RatingComponent} from "../../../../../shared/rating/rating.component";
import {TrashService} from "../../../../services/trash.service";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss']
})
export class DetailComponent implements OnInit {
  public contentType: string = '';
  public content?: Partial<MovieModel | TvModel | any>;
  public recomendedContentList: Array<PaginationModel> = [];
  public video?: ContentModel;
  public isLoading: boolean = true;
  public movie?: MovieModel;
  public status?: string;
  public rating?: any;
  public is_favorite?: boolean;
  public user?: User;
  public isInTrash?: boolean;

  @ViewChild('matTrailerDialog') matTrailerDialog!: TemplateRef<any>;

  constructor(
    private moviesService: MoviesService,
    private route: ActivatedRoute,
    private router: Router,
    private sanitezer: DomSanitizer,
    public trailerDialog: MatDialog,
    private storage: StorageService,
    private dialog: MatDialog,
    private trashService: TrashService
  ) {
    this.contentType = this.router.url.split('/')[1];

  }

  ngOnInit() {
    this.user = this.storage.getUser();
    this.route.params.subscribe(params => {
      const id = params['id'];
      if (this.contentType === 'movies') {
        this.getMovieById(id);
        this.getMovieVideoById(id);
        this.getMovieRecommendationsById(id);
        if (this.user != null) {
          this.getMovieDetailsForUsers(id, this.user.id);
          this.getMovieFromTrash(id);
        }
      }

    });
  }

  private getMovieById(id: string) {
    this.isLoading = true;
    this.moviesService.getMovieById(id).subscribe((movie: any) => {
      this.content = this.moviesService.parseMovie(movie);
      this.isLoading = false;
    });
  }

  private getMovieVideoById(id: string) {
    this.moviesService.getMovieVideos(id).pipe(take(1)).subscribe((res: any) => {
      if (res?.results?.length > 0) {
        const trailerList = res.results.filter((video: any) => video.type === 'Trailer');
        this.video = trailerList[0];
        this.video!.url = this.sanitezer.bypassSecurityTrustResourceUrl(`https://www.youtube.com/embed/${this.video!.key}`);
      } else {
        this.video = undefined;
      }
    });
  }

  private getMovieDetailsForUsers(movieId: any, userId: any) {
    this.moviesService.getMovieDetailsForUser(movieId, userId)?.pipe(catchError(err => {
      this.status = "Not watched";
      return throwError(() => new Error(err));
    })).subscribe((data: any) => {
      this.status = data.status;
      this.rating = data.rating;
      this.is_favorite = data.is_favorite;
    });
  }

  private getMovieRecommendationsById(id: string) {
    this.moviesService.getRecommendedMovies(id, 1).pipe(take(1)).subscribe((res: any) => {
      this.recomendedContentList = res.results.slice(0, 12);
    });
  }

  private getMovieFromTrash(movie_id: any) {
    if (this.user !== undefined) {
      this.trashService.getMovieById(this.user.id, movie_id).subscribe((r) => {
        this.isInTrash = !!r;
      });
    }

  }

  public openDialog(): void {
    const dialogRef = this.trailerDialog.open(this.matTrailerDialog, {});
    dialogRef.disableClose = false;
  }

  public addMovie() {
    let body = {
      "status": this.status,
      "rating": this.rating,
      "is_favorite": this.is_favorite
    };
    this.moviesService.addMovieToUser(this.content?.['id'], this.user?.id, body).subscribe();
  }

  public setFavorite(value: boolean) {
    if (this.status === "Watched") {
      this.is_favorite = value;
      this.addMovie();
    }
  }

  public openRatingDialog() {
    let dialogRating = this.dialog.open(RatingComponent, {
      minWidth: '200px',
      width: '30vw',
      maxWidth: '600px',
      height: 'auto',
      data: {
        rating: this.rating != undefined ? this.rating : 0,
        movieId: this.content?.['id'],
        userId: this.user?.id,
        contentType: this.contentType,
        status: this.status,
        title: this.content?.['title']
      },
      backdropClass: 'backdropBackground'
    }).afterClosed().subscribe(rating => {
      if (rating != null) {
        this.rating = rating;
      }
    });
  }

  public addMovieToTrash() {
    if(this.user !== undefined) {
      this.trashService.addMovieToTrash(this.user?.id, this.content?.['id']).subscribe(() => {
        this.isInTrash = true;
      });
    }
  }

  public deleteMovieFromTrash() {
    if (this.user !== undefined) {
      this.trashService.deleteMovieFromTrash(this.user.id, this.content?.['id']).subscribe(() => {
        this.isInTrash = false;
      });
    }
  }
}
