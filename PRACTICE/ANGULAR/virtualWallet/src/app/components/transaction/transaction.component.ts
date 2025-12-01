import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { TransactionData } from 'src/app/models/TransactionData';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { TransactionDataService } from 'src/app/services/transaction-data.service';

@Component({
  selector: 'app-transaction',
  templateUrl: './transaction.component.html',
  styleUrls: ['./transaction.component.css']
})
export class TransactionComponent implements OnInit, AfterViewInit {

  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  transactionDataSource = new MatTableDataSource<TransactionData>();
  columnsToDisplay = ['no', 'date', 'type', 'symbol', 'price', 'amount','delete'];
  disableDeleteData:boolean=true;
  constructor(private transactionService: TransactionDataService ) {}

  ngAfterViewInit() {
    this.transactionDataSource.sort = this.sort; 
    this.transactionDataSource.paginator = this.paginator;
  }

  ngOnInit(): void {
    this.retrieveTransactionHistory();
  }

  private retrieveTransactionHistory() {
    this.transactionService
      .getTransactionHistory()
      .subscribe((items) => {
        this.transactionDataSource.data = items;
        this.disableDeleteData=items.length==0;
      });
  }

  filteringGrid(ev: any) {
    console.log(ev.value.trim());
    this.transactionDataSource.filter=ev.value.trim().toLocaleLowerCase();
  }
  deleteTransaction(element:TransactionData){
    this.transactionService.removeTransactionFromHistory(element);
    this.retrieveTransactionHistory(); 
  }
  removeAllTransactions()
  { 
    this.transactionService.deleteAllTransactionsFromHistory();
    this.retrieveTransactionHistory();
  }

}
