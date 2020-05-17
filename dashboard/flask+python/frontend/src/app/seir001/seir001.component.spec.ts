import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Seir001Component } from './seir001.component';

describe('Seir001Component', () => {
  let component: Seir001Component;
  let fixture: ComponentFixture<Seir001Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Seir001Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Seir001Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
