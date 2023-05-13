import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from './material/material.module';
import { RouterModule } from '@angular/router';
import { MovieCardComponent } from './movie-card/movie-card.component';
import { ImageMissingDirective } from './directives/ImageMissing.directive';
import { ActorSortPipe } from './pipes/actorSort.pipe';

@NgModule({
  imports: [
    CommonModule,
    MaterialModule,
    RouterModule
  ],
  exports: [
    MaterialModule,
    CommonModule,
    MovieCardComponent,
    ImageMissingDirective,
    ActorSortPipe
  ],
  declarations: [
    MovieCardComponent,
    ImageMissingDirective,
    ActorSortPipe
  ]
})
export class SharedModule { }
