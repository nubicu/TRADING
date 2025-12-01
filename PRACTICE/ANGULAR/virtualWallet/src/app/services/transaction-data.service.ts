import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { TransactionData } from '../models/TransactionData';

@Injectable({
  providedIn: 'root'
})
export class TransactionDataService {

  constructor() { }

  public getTransactionHistory(): Observable<TransactionData[]> {
    var storedItems = localStorage.getItem('transactions');
    if(storedItems)
    {
      return of(JSON.parse(storedItems)); 
    }else return of([]);

  }
  public addTransactionToHistory(transaction:TransactionData):void {
    let transactionData : TransactionData[] = JSON.parse(this.RetrieveTransactionsFromStorage());
    if (transactionData){
     transaction.no = transactionData.sort((a,b) => b.no - a.no )[0].no + 1;
     transactionData.push(transaction);
    } else {
      transactionData=[];
      transactionData.push(transaction);
    }
    localStorage.setItem('transactions', JSON.stringify(transactionData))
    return;
  }

  public removeTransactionFromHistory(transaction : TransactionData) : void {
    let transactionData : TransactionData[] = JSON.parse(this.RetrieveTransactionsFromStorage()); 
    if (transactionData){
      localStorage.setItem('transactions', JSON.stringify(transactionData.filter( (a) => a.no !== transaction.no)))
    }
    return;
  }
  public deleteAllTransactionsFromHistory():void {

    localStorage.removeItem('transactions')
    return;
  }
  private RetrieveTransactionsFromStorage():string{
    return localStorage.getItem('transactions');
  };

}
