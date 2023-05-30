import {Component, Input, OnInit} from '@angular/core';
import {MoviesService} from "../../../../services/movies.service";
import {TvShowsService} from "../../../../services/tv-shows.service";

@Component({
  selector: 'app-poster-card',
  templateUrl: './poster-card.component.html',
  styleUrls: ['./poster-card.component.scss']
})
export class PosterCardComponent implements OnInit {
  @Input() public model: any;
  public apiModel: any;
  @Input() public contentType: string = "";
  @Input() public trashFilter: string = "";
  public isMovie: boolean = true;
  public numberOfStars: Array<number> = [];
  public maxRatingArray: any = [];
  private maxRating = 10;
  constructor(
    private moviesService: MoviesService,
    private tvService: TvShowsService
  ) {
  }

  ngOnInit() {
    if (this.contentType === 'movies' || this.trashFilter === 'movies') {
      this.isMovie = true;
      this.moviesService.getMovieById(this.model['movie'].id).subscribe(
        {
          next: (response: any) => {
            this.apiModel = response;
          },
          error: (_: any) => {

          }
        }
      );

    } else if (this.contentType === "tv-shows" || this.trashFilter === 'tv-shows') {
      this.isMovie = false;
      this.tvService.getTvById(this.model['tv_show'].id).subscribe(
        {
          next: (response: any) => {
            this.apiModel = response;
          },
          error: (_: any) => {

          }
        }
      );
    }
    if (this.model.rating === undefined) {
      this.model.rating = 0;
    }

    this.numberOfStars = Array(this.model.rating).fill(0).map((x, i) => i);
    this.maxRatingArray = Array(this.maxRating - this.numberOfStars.length).fill(0);
  }

}
