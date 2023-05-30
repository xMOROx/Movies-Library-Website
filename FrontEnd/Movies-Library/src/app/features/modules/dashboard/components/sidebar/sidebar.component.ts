import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {AuthService} from "../../../../../authentication/services/auth.service";

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  public isExpanded: boolean = false;
  public componentName: string = 'Dashboard';
  constructor(
    private router: Router,
    public auth: AuthService
  ) {
  }

  ngOnInit() {
    this.componentName;

  }

}
