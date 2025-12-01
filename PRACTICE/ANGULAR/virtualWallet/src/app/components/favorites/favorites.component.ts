import { Component, Input, OnInit } from '@angular/core';
import { CoinInfo } from './../../models/CoinsInfo';
import { SharedDataService } from './../../services/shared-data.service';

@Component({
  selector: 'app-favorites',
  templateUrl: './favorites.component.html',
  styleUrls: ['./favorites.component.css']
})
export class FavoritesComponent implements OnInit {

  @Input() coins: CoinInfo[] = [];

  favorites: CoinInfo[] = [];
  
  favoriteIds: string[] = [
    "chiliz", "dogecoin", "shiba-inu", "cardano"
  ];

  myCoins: {[key: string]: number} = {
    "chiliz": 104,
    "dogecoin": 687,
    "shiba-inu": 1810000,
    "cardano": 34
  }

  constructor(private sharedData: SharedDataService) { }

  ngOnInit(): void {
  }

  ngOnChanges(): void {
    this.setFavorites();
  }

  setFavorites() {
    this.sharedData.getCoin().subscribe((ids): void => {
      this.favorites = [];

      if(!ids) {
        return ;
      }

      if (Array.isArray(ids)) {
        ids.forEach((id: string) => {
          const coin: CoinInfo =  this.coins.find((coin: CoinInfo) => {
            return coin.id === id;
          });
          coin.my_currency = (this.myCoins[coin.id] || 0) * coin.current_price;
          this.favorites.push(coin);
        });
      }

    })
  }
}
