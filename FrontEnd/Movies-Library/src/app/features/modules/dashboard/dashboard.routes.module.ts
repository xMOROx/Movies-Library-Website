import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import {SidebarComponent} from "./components/sidebar/sidebar.component";
import {ContentComponent} from "./components/content/content.component";
import {SettingsComponent} from "./components/settings/settings.component";
import {DashboardComponent} from "./dashboard.component";

const dashboardRoutes: Routes = [
  {
    path: '',
    component: SidebarComponent,
    children: [
      {path: '', component: DashboardComponent},
      {path: 'movies', component: ContentComponent},
      {path: 'TV-shows', component: ContentComponent},
      {path: 'trash', component: ContentComponent},
      {path: 'settings', component: SettingsComponent},

    ]
  },
  {
    path: '**',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(dashboardRoutes)
  ],
  exports: [RouterModule]
})

export class DashboardRoutesModule { }
