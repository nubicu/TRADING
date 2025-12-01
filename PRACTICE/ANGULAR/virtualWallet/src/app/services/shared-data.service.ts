import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, Subject } from 'rxjs';
//import { CoinsInfo } from './../models/CoinsInfo';
import { TransactionData } from '../models/TransactionData';

@Injectable({
  providedIn: 'root'
})
export class SharedDataService {

  public coin$ = new BehaviorSubject<string[]>(undefined);

  public selectedCoin$ = new Subject<string>();
  private storageBudget = +localStorage.getItem('budget');
  private budget$ = new BehaviorSubject<number>(this.storageBudget);
  public showHeaderBudgetAdd = new BehaviorSubject<boolean>(true);

  constructor() { }

  public getCoin(): Observable<string[]> {
    return this.coin$.asObservable();
  }

  public getSelectedCoin(): Observable<string> {
    return this.selectedCoin$.asObservable();
  }

  public addBudget(value: number) {
    const currentBudget = (this.storageBudget += value);
    this.storageBudget = currentBudget;
    localStorage.setItem('budget', currentBudget.toString());
    this.budget$.next(currentBudget);
  }

  public subtractBudget(value: number) {
    const currentBudget = (this.storageBudget -= value);
    this.storageBudget = currentBudget;
    localStorage.setItem('budget', currentBudget.toString());
    this.budget$.next(currentBudget);
  }

  public getBudget(): Observable<number> {
    return this.budget$.asObservable();
  }
}
