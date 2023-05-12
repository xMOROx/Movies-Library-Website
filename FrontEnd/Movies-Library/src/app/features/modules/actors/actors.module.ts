import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActorsComponent } from './actors.component';
import { ActorComponent } from './components/actor/actor.component';
import { ActorsRoutesModule } from 'src/app/features/modules/actors/actors.routes.module';
import { SharedModule } from 'src/app/shared/shared.module';
import { HttpClientModule } from '@angular/common/http';
import { ActorCardComponent } from './components/actor-card/actor-card.component';

@NgModule({
  imports: [
    CommonModule,
    ActorsRoutesModule,
    SharedModule,
    HttpClientModule
  ],
  exports: [ActorsComponent, ActorComponent, ActorCardComponent],
  declarations: [ActorsComponent, ActorComponent, ActorCardComponent]
})
export class ActorsModule { }
