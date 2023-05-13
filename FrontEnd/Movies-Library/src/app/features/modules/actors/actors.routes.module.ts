import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { ActorsComponent } from './actors.component';
import { ActorComponent } from './components/actor/actor.component';

const actorRoutes: Routes = [
    {
        path: '',
        children: [
            { path: '', component: ActorsComponent },
            { path: ':actorId', component: ActorComponent },
        ]
    },
];

@NgModule({
    imports: [
        RouterModule.forChild(actorRoutes)
    ],
    exports: [RouterModule]
})

export class ActorsRoutesModule { }