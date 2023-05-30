import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { SidebarComponent } from "./components/sidebar/sidebar.component";
import { ContentComponent } from "./components/content/content.component";
import { DashboardComponent } from "./dashboard.component";
import { IsLoggedGuard } from "../../../authentication/guards/is-logged.guard";
import { ManageUsersComponent } from './components/manage-users/manage-users.component';
import { IsAdminGuard } from '../../../authentication/guards/is-admin.guard';

const dashboardRoutes: Routes = [
  {
    path: '',
    component: SidebarComponent,
    canActivateChild: [IsLoggedGuard],
    children: [
      { path: '', component: DashboardComponent },
      { path: 'movies', component: ContentComponent },
      { path: 'tv-shows', component: ContentComponent },
      { path: 'trash', component: ContentComponent },
      { path: 'recommended', component: ContentComponent },
      { path: 'manage-users', component: ManageUsersComponent, canActivate: [IsAdminGuard] }
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

export class DashboardRoutesModule {
}
