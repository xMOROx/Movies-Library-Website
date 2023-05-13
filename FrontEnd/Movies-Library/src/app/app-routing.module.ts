import { NgModule } from '@angular/core';
import { RouterModule, Routes } from "@angular/router";
import { AppComponent } from "./app.component";
import { PageNotFoundComponent } from "src/app/core/components/page-not-found/page-not-found.component";
import { HomeComponent } from './features/home/home.component';


const routes: Routes = [
  { path: '', component: HomeComponent, pathMatch: 'full' },
  { path: '404', component: PageNotFoundComponent, pathMatch: 'full' },

  { path: 'movies', loadChildren: () => import('./features/modules/content/content.module').then(m => m.ContentModule) },
  { path: 'tv-shows', loadChildren: () => import('./features/modules/content/content.module').then(m => m.ContentModule) },
  { path: 'actors', loadChildren: () => import('./features/modules/actors/actors.module').then(m => m.ActorsModule) },
  { path: 'user-profile', loadChildren: () => import('./features/modules/users/users.module').then(m => m.UsersModule) },

  { path: '**', redirectTo: '404' }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
