import { Component } from '@angular/core';
import { CoinInfo } from './models/CoinsInfo';
import { CoinsService } from './services/coins.service';
import { fromEvent, interval, switchMap, take } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'virtualWallet';
  coins: CoinInfo[] = [];
  
  constructor(private coinsService: CoinsService) {
  }

  ngOnInit(): void {
    this.getCoinsData();
    window.setInterval(this.getCoinsData.bind(this), 50000);
  }

  getCoinsData() {
    this.coinsService.getCoins().subscribe((response) => {
      this.coins = response;
    })
  }
}
