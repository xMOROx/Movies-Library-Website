import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-movie-card',
  templateUrl: './movie-card.component.html',
  styleUrls: ['./movie-card.component.scss']
})
export class MovieCardComponent implements OnInit {

  @Input() public model: any;
  @Input() public isMovie: boolean = true;


  constructor() { }

  ngOnInit() {
  }

}
