import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent implements OnInit {
  public socialData = [
    { url: 'https://github.com/xMOROx/Movies-Library-Website', name: '', img: 'assets/img/github-logo.png' },
  ];
  constructor() { }

  ngOnInit() {
  }

}
