import { NgModule } from '@angular/core';
import { RouterModule, Routes } from "@angular/router";
import { AppComponent } from "./app.component";
import { PageNotFoundComponent } from "src/app/core/components/page-not-found/page-not-found.component";
import { HomeComponent } from './features/home/home.component';


const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: '', loadChildren: () => import('./authentication/authentication.module').then(m => m.AuthenticationModule) },
  { path: 'movies', loadChildren: () => import('./features/modules/content/content.module').then(m => m.ContentModule) },
  { path: 'tv-shows', loadChildren: () => import('./features/modules/content/content.module').then(m => m.ContentModule) },
  { path: 'actors', loadChildren: () => import('./features/modules/actors/actors.module').then(m => m.ActorsModule) },
  { path: 'user-profile', loadChildren: () => import('./features/modules/users/users.module').then(m => m.UsersModule) },
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
