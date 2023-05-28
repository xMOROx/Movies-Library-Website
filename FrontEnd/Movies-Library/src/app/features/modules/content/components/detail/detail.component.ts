import {Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {MatDialog, MatDialogRef} from '@angular/material/dialog';
import {DomSanitizer} from '@angular/platform-browser';
import {ActivatedRoute, Router} from '@angular/router';
import {take, throwError} from 'rxjs';
import {MoviesService} from 'src/app/features/services/movies.service';
import {ContentModel} from '../../models/Content.model';
import {MovieModel} from '../../models/Movie.model';
import {PaginationModel} from '../../models/pagination.model';
import {TvModel} from '../../models/Tv.model';
import {User} from "../../../../../authentication/models/User";
import {StorageService} from "../../../../../authentication/services/storage.service";
import {catchError} from "rxjs/operators";
import {RatingComponent} from "../../../../../shared/components/rating/rating.component";
import {TrashService} from "../../../../services/trash.service";
import {TvShowsService} from "../../../../services/tv-shows.service";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss']
})
export class DetailComponent implements OnInit {
  public contentType: string = '';
  public content?: Partial<MovieModel | TvModel | any>;
  public recommendedContentList: Array<PaginationModel> = [];
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
    private sanitizer: DomSanitizer,
    public trailerDialog: MatDialog,
    private storage: StorageService,
    private dialog: MatDialog,
    private trashService: TrashService,
    private tvService: TvShowsService
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
          this.getContentFromTrash(id);
        }
      } else {
        this.getTvById(id);
        this.getTvVideoById(id);
        this.getTvRecommendationsById(id);

        if (this.user != null) {
          this.getTvDetailsForUsers(id, this.user.id);
          this.getContentFromTrash(id);
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

  private getTvById(id: string) {
    this.isLoading = true;
    this.tvService.getTvById(id).subscribe((tv: any) => {
      this.content = this.tvService.parseTv(tv);
      this.isLoading = false;
    });
  }

  private getMovieVideoById(id: string) {
    this.moviesService.getMovieVideos(id).pipe(take(1)).subscribe((res: any) => {
      if (res?.results?.length > 0) {
        const trailerList = res.results.filter((video: any) => video.type === 'Trailer');
        this.video = trailerList[0];
        this.video!.url = this.sanitizer.bypassSecurityTrustResourceUrl(`https://www.youtube.com/embed/${this.video!.key}`);
      } else {
        this.video = undefined;
      }
    });
  }

  private getTvVideoById(id: string) {
    this.tvService.getTvVideos(id).pipe(take(1)).subscribe((res: any) => {
      if (res?.results?.length > 0) {
        const trailerList = res.results.filter((video: any) => video.type === 'Trailer');
        this.video = trailerList[0];
        this.video!.url = this.sanitizer.bypassSecurityTrustResourceUrl(`https://www.youtube.com/embed/${this.video!.key}`);
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

  private getTvDetailsForUsers(tvId: any, userId: any) {
    this.tvService.getTvDetailsForUser(tvId, userId)?.pipe(catchError(err => {
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
      this.recommendedContentList = res.results.slice(0, 12);
    });
  }

  private getTvRecommendationsById(id: string) {
    this.tvService.getRecommendedTv(id, 1).pipe(take(1)).subscribe((res: any) => {
      this.recommendedContentList = res.results.slice(0, 12);
    });
  }

  private getContentFromTrash(movie_id: any) {
    if (this.user !== undefined) {
      this.trashService.getTrashById(this.user.id, movie_id, this.contentType).subscribe(
        {
          next: (r) => {
            this.isInTrash = !!r;
          },
          error: (err) => {

          }
        }
      );
    }

  }

  public openDialog(): void {
    const dialogRef = this.trailerDialog.open(this.matTrailerDialog, {
      backdropClass: 'backdropBackground',
    });
    dialogRef.disableClose = false;
  }

  public addContent() {
    let body = {
      "status": this.status,
      "rating": this.rating,
      "is_favorite": this.is_favorite
    };
    if (this.contentType === 'movies') {
      this.moviesService.addMovieToUser(this.content?.['id'], this.user?.id, body).subscribe();
    } else {
      this.tvService.addTvToUser(this.content?.['id'], this.user?.id, body).subscribe();
    }
  }

  public setFavorite(value: boolean) {
    if (this.status === "Watched") {
      this.is_favorite = value;
      this.addContent();
      return;
    }
    alert("You can't set favorite to a movie you haven't watched yet");
  }

  public openRatingDialog() {
    let dialogRating = this.dialog.open(RatingComponent, {
      minWidth: '200px',
      width: '30vw',
      maxWidth: '600px',
      height: 'auto',
      data: {
        rating: this.rating != undefined ? this.rating : 0,
        contentId: this.content?.['id'],
        userId: this.user?.id,
        contentType: this.contentType,
        status: this.status,
        title: this.content?.['title'] ?? this.content?.['name']
      },
      backdropClass: 'backdropBackground'
    }).afterClosed().subscribe(rating => {
      if (rating != null) {
        this.rating = rating;
      }
    });
  }

  public addContentToTrash() {
    if (this.user !== undefined) {
      this.trashService.addContentToTrash(this.user?.id, this.content?.['id'], this.contentType).subscribe(() => {
        this.isInTrash = true;
      });
    }
  }

  public deleteContentFromTrash() {
    if (this.user !== undefined) {
      this.trashService.deleteContentFromTrash(this.user.id, this.content?.['id'], this.contentType).subscribe(() => {
        this.isInTrash = false;
      });
    }
  }

  public getWatchTime(runtime: number): string {
    let result = ""
    if (Math.floor(runtime / 60) > 0) {
      result += Math.floor(runtime / 60).toString() + "h ";
    }
    return result + (runtime % 60).toString() + "min";
  }
}
