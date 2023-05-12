import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { ContentComponent } from './content.component';
import { DetailComponent } from './components/detail/detail.component';
import { MovieDetailsComponent } from './components/movie-views/movie-details/movie-details.component';

const contentRoutes: Routes = [
    {
        path: '',
        children: [
            { path: '', component: ContentComponent },
            { path: ':url', component: DetailComponent },
            { path: ':id', component: MovieDetailsComponent }
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