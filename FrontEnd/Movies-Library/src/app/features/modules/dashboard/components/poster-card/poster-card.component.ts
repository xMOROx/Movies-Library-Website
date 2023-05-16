import {Component, Input, OnInit} from '@angular/core';
import {MoviesService} from "../../../../services/movies.service";

@Component({
  selector: 'app-poster-card',
  templateUrl: './poster-card.component.html',
  styleUrls: ['./poster-card.component.scss']
})
export class PosterCardComponent implements OnInit {
  @Input() public model: any;
  public apiModel: any;
  @Input() public contentType: string = "";
  public isMovie: boolean = true;
  public numberOfStars: Array<number> = [];
  constructor(
    private moviesService: MoviesService,
  ) {
  }

  ngOnInit() {
    if (this.contentType === 'movies' || this.contentType === 'trash') {
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

    } else if (this.contentType === "TV-shows") {
      this.isMovie = false;
    }
    this.numberOfStars = Array(this.model.rating).fill(0).map((x, i) => i);

  }

}
