import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActorsComponent } from './actors.component';
import { ActorComponent } from './actor/actor.component';
import { MaterialModule } from 'src/app/shared/material/material.module';
import { ActorsRoutesModule } from 'src/app/features/actors/actors.routes.module';

@NgModule({
  imports: [
    CommonModule,
    MaterialModule,
    ActorsRoutesModule

  ],
  declarations: [ActorsComponent, ActorComponent]
})
export class ActorsModule { }
