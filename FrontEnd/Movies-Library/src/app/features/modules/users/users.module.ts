import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UsersComponent } from './users.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { ProfileComponent } from './components/profile/profile.component';
import { ContentModule } from '../content/content.module';
import { UsersRoutesModule } from './users.routes.module';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    UsersRoutesModule,
    HttpClientModule,
    ContentModule,

  ],
  exports: [UsersComponent, ProfileComponent],
  declarations: [UsersComponent, ProfileComponent]
})
export class UsersModule { }
