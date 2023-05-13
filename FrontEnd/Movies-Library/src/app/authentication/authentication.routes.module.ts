import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';


const authenticationRoutes: Routes = [
    {
        path: '',
        children: [
            { path: 'login', component: LoginComponent },
            { path: 'register', component: RegisterComponent }
        ]
    },
];

@NgModule({
    imports: [
        RouterModule.forChild(authenticationRoutes)
    ],
    exports: [RouterModule]
})

export class AuthenticationRoutesModule { }