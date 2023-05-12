/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { ActorsService } from './actors.service';

describe('Service: Actors', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ActorsService]
    });
  });

  it('should ...', inject([ActorsService], (service: ActorsService) => {
    expect(service).toBeTruthy();
  }));
});
