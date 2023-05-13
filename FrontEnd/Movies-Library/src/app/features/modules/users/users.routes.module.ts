import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { ProfileComponent } from './components/profile/profile.component';
import { UserMoviesComponent } from './components/user-movies/user-movies.component';

const usersRoutes: Routes = [
    {
        path: '',
        children: [
            { path: ':id', component: ProfileComponent },
            { path: ':id/movies', component: UserMoviesComponent },
        ]
    },
];

@NgModule({
    imports: [
        RouterModule.forChild(usersRoutes)
    ],
    exports: [RouterModule]
})

export class UsersRoutesModule { }