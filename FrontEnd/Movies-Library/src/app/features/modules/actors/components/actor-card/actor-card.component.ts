import { Component, Input, OnInit } from '@angular/core';
import { ActorModel } from '../../models/Actor.model';

@Component({
  selector: 'app-actor-card',
  templateUrl: './actor-card.component.html',
  styleUrls: ['./actor-card.component.scss']
})
export class ActorCardComponent implements OnInit {
  @Input() public model?: ActorModel;

  constructor() { }

  ngOnInit() {
  }

}
