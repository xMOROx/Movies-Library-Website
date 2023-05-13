import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MovieDetailsForUserComponent } from './movie-details-for-user.component';

describe('MovieDetailsForUserComponent', () => {
  let component: MovieDetailsForUserComponent;
  let fixture: ComponentFixture<MovieDetailsForUserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MovieDetailsForUserComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(MovieDetailsForUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
