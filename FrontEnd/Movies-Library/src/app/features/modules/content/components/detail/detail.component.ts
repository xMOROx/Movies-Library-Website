import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { take } from 'rxjs';
import { MoviesService } from 'src/app/features/services/movies.service';
import { ContentModel } from '../../models/Content.model';
import { MovieModel } from '../../models/Movie.model';
import { PaginationModel } from '../../models/pagination.model';
import { TvModel } from '../../models/Tv.model';

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

  @ViewChild('matTrailerDialog') matTrailerDialog!: TemplateRef<any>;

  constructor(
    private moviesService: MoviesService,
    private route: ActivatedRoute,
    private router: Router,
    private sanitezer: DomSanitizer,
    public trailerDialog: MatDialog
  ) {
    this.contentType = this.router.url.split('/')[1];

  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      const id = params['id'];
      if (this.contentType === 'movies') {
        this.getMovieById(id);
        this.getMovieVideoById(id);
        this.getMovieRecommendationsById(id);
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

  private getMovieRecommendationsById(id: string) {
    this.moviesService.getRecommendedMovies(id, 1).pipe(take(1)).subscribe((res: any) => {
      this.recomendedContentList = res.results.slice(0, 12);
    });
  }

  public openDialog(): void {
    const dialogRef = this.trailerDialog.open(this.matTrailerDialog, {});
    dialogRef.disableClose = false;
  }
}
