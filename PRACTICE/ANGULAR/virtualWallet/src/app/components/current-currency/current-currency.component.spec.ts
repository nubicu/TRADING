import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CurrentCurrencyComponent } from './current-currency.component';

describe('CurrentCurrencyComponent', () => {
  let component: CurrentCurrencyComponent;
  let fixture: ComponentFixture<CurrentCurrencyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CurrentCurrencyComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CurrentCurrencyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
