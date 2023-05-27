import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ContentComponent } from './content.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { DetailComponent } from './components/detail/detail.component';
import { FilterByStatusPipe } from './pipes/filter-by-status.pipe';
import { ContentRoutesModule } from './content.routes.module';
import { HttpClientModule } from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    ContentRoutesModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  exports: [
    ContentComponent,
    DetailComponent,
    FilterByStatusPipe,
  ],
  declarations: [
    ContentComponent,
    DetailComponent,
    FilterByStatusPipe,
  ]
})
export class ContentModule { }
