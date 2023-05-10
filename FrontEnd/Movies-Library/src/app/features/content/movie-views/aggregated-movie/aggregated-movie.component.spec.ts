import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AggregatedMovieComponent } from './aggregated-movie.component';

describe('AggregatedMovieComponent', () => {
  let component: AggregatedMovieComponent;
  let fixture: ComponentFixture<AggregatedMovieComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AggregatedMovieComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AggregatedMovieComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
