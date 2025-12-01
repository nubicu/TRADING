import { Component, Input, OnInit } from '@angular/core';
import { CoinInfo } from './../../models/CoinsInfo';
import { SharedDataService } from 'src/app/services/shared-data.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  
  @Input() coins: CoinInfo[] = [];
  showCurrency:boolean;
  
  constructor(private sharedDataService:SharedDataService) { }

  ngOnInit(): void {
    this.sharedDataService.showHeaderBudgetAdd.subscribe(s=>
      this.showCurrency=s
    )
  }

}
