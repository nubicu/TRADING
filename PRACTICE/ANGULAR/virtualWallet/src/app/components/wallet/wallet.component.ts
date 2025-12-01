import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatSelectChange } from '@angular/material/select';
import { Observable } from 'rxjs';
import { CoinInfo } from 'src/app/models/CoinsInfo';
import { CoinsService } from 'src/app/services/coins.service';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { TransactionDataService } from 'src/app/services/transaction-data.service';

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.css']
})
export class WalletComponent implements OnInit, OnDestroy {

  public coinId: string[];
  public status: number;
  public budget: number;
  public coins$: Observable<CoinInfo[]>;
  public selectedCoin: number = 0;
  public totalCost: number = 0;
  public overPrice: boolean = false;
  public amount: any;
  public coinName: string = "";
  public hasAmount: boolean = false;
  
  constructor(
    private sharedData: SharedDataService, 
    private coinService: CoinsService,
    private transactionHistory:TransactionDataService,
    ) { }

  ngOnInit(): void {
    this.sharedData.getCoin().subscribe(ids => {
      this.coinId = ids;
    })
    this.sharedData.showHeaderBudgetAdd.next(true);
    this.sharedData.getBudget().subscribe((currentBudget) => {
      this.status = currentBudget;
      this.budget = currentBudget;
      this.resetOverPrice();
    });
    this.coins$ = this.coinService.getCoins();
  }

  calculateTotalPrice(evt: any) {
    this.amount = +evt.value;
    this.totalCost = this.selectedCoin * +this.amount;
    this.overPrice = this.totalCost > this.budget;
    this.hasAmount = +this.amount > 0;
  }

  resetValues(selectedCoin:MatSelectChange) {
    this.totalCost = 0;
    this.overPrice = false;
    this.amount = '';
    this.coinName = selectedCoin.source.triggerValue;
  }

  buyCoins() { 
    this.performTransactionPersistence("BUY")
  }
  sellCoins() {  
    this.performTransactionPersistence("SELL") 
  }

  private performTransactionPersistence(operation:string):void
  {
    this.budget -= this.selectedCoin * +this.amount;
    if(operation == "BUY"){
    this.sharedData.subtractBudget(this.selectedCoin * +this.amount);
    } else
    this.sharedData.addBudget(this.selectedCoin * +this.amount);
    this.transactionHistory.addTransactionToHistory({
      no:1,
      date:new Date(),
      symbol:this.coinName.toLocaleUpperCase(),
      price:this.selectedCoin,
      amount:this.amount,
      type:operation
    });
  }
  private resetOverPrice(){
    this.overPrice = this.totalCost > this.budget;
  }

  ngOnDestroy(): void {
    this.sharedData.showHeaderBudgetAdd.next(false);
   }

}

// no:number,
// date:Date,
// type:string,
// symbol:string,
// price:number,
// amount:number
