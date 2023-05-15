import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import { SharedModule } from "../../../shared/shared.module";
import { DashboardRoutesModule } from "./dashboard.routes.module";
import { SidebarComponent } from "./components/sidebar/sidebar.component";
import { MaterialModule } from "../../../shared/material/material.module";
import { ContentComponent } from "./components/content/content.component";
import { SettingsComponent } from "./components/settings/settings.component";
import {PosterCardComponent} from "./components/poster-card/poster-card.component";
import {UsersModule} from "../users/users.module";

@NgModule({
    imports: [
        DashboardRoutesModule,
        CommonModule,
        SharedModule,
        MaterialModule,
        UsersModule
    ],
  declarations: [DashboardComponent, SidebarComponent, ContentComponent, SettingsComponent, PosterCardComponent]
})
export class DashboardModule { }
