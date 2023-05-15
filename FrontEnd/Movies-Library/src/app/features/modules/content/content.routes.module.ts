import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { ContentComponent } from './content.component';
import { DetailComponent } from './components/detail/detail.component';

const contentRoutes: Routes = [
    {
        path: '',
        children: [
            { path: '', component: ContentComponent },
            { path: ':id', component: DetailComponent }
        ]
    },
];

@NgModule({
    imports: [
        RouterModule.forChild(contentRoutes)
    ],
    exports: [RouterModule]
})

export class ContentRoutesModule { }
