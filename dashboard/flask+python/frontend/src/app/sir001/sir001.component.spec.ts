import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Sir001Component } from './sir001.component';

describe('Sir001Component', () => {
  let component: Sir001Component;
  let fixture: ComponentFixture<Sir001Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Sir001Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Sir001Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
