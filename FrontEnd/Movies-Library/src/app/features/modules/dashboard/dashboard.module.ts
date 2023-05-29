import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import { SharedModule } from "../../../shared/shared.module";
import { DashboardRoutesModule } from "./dashboard.routes.module";
import { SidebarComponent } from "./components/sidebar/sidebar.component";
import { MaterialModule } from "../../../shared/material/material.module";
import { ContentComponent } from "./components/content/content.component";
import { PosterCardComponent } from "./components/poster-card/poster-card.component";
import { ManageUsersComponent } from "./components/manage-users/manage-users.component";
import { UsersModule } from "../users/users.module";
import {FormsModule} from "@angular/forms";

@NgModule({
  imports: [
    DashboardRoutesModule,
    CommonModule,
    SharedModule,
    MaterialModule,
    UsersModule,
    FormsModule
  ],
  declarations: [DashboardComponent, SidebarComponent, ContentComponent, PosterCardComponent, ManageUsersComponent]
})
export class DashboardModule { }
