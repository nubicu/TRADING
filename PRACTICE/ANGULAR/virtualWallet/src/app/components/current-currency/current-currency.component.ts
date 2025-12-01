import { Component, OnInit } from '@angular/core';
import { SharedDataService } from 'src/app/services/shared-data.service';

@Component({
  selector: 'app-current-currency',
  templateUrl: './current-currency.component.html',
  styleUrls: ['./current-currency.component.css']
})
export class CurrentCurrencyComponent implements OnInit {

  constructor(private sharedDataService: SharedDataService) { }

  ngOnInit(): void {
  }

  addMoneyToWallet(el: any) {
    this.sharedDataService.addBudget(+el.value);
    el.value = 0;
  }

  removeMoneyFromWallet(el: any) {
    this.sharedDataService.subtractBudget(+el.value);
    el.value = 0;
  }
}
