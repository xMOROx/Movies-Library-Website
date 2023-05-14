import {Component, Inject, Input} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {MoviesService} from "../../features/services/movies.service";

@Component({
  selector: 'app-rating',
  templateUrl: './rating.component.html',
  styleUrls: ['./rating.component.scss']
})
export class RatingComponent {
  @Input() maxRating: number = 10;
  public maxRatingArray: any = [];
  @Input() public selectedStars: number;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any,
              private moviesService: MoviesService,
              private dialog: MatDialogRef<RatingComponent>) {
    this.maxRatingArray = Array(this.maxRating).fill(0);
    this.selectedStars = data.rating;
  }

  handleMouseEnter(index: number) {
    this.selectedStars = index + 1;
  }

  handleMouseLeave() {
    this.selectedStars = this.data.rating;
  }

  rate(index: number) {
    if (this.data.contentType === "movies") {
      let body = {
        "rating": index + 1
      };
      if (this.data.status === "Watched") {
        this.moviesService.addMovieToUser(this.data.movieId, this.data.userId, body).subscribe(() => {
          this.dialog.close(index + 1);
        });
        return;
      }
      alert("You have to watch the movie first!");

    }
  }

  close() {
    this.dialog.close();
  }

}
