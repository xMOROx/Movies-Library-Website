import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { ProfileComponent } from './components/profile/profile.component';
import {IsLoggedGuard} from "../../../authentication/guards/is-logged.guard";

const usersRoutes: Routes = [
    {
        path: '',
        canActivateChild: [IsLoggedGuard],
        children: [
            { path: ':userId', component: ProfileComponent },
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
