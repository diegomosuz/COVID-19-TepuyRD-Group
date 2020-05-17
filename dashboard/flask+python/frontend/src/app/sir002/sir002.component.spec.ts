import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Sir002Component } from './sir002.component';

describe('Sir002Component', () => {
  let component: Sir002Component;
  let fixture: ComponentFixture<Sir002Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Sir002Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Sir002Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
