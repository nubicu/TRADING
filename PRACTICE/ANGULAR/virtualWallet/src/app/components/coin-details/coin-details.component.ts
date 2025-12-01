import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { CoinInfo } from './../../models/CoinsInfo';
import { CoinsService } from './../../services/coins.service';
import { SharedDataService } from './../../services/shared-data.service';

@Component({
  selector: 'app-coin-details',
  templateUrl: './coin-details.component.html',
  styleUrls: ['./coin-details.component.css']
})
export class CoinDetailsComponent implements OnInit {

  displayedColumns: string[] = ['info', 'image', 'name', 'current_price', 'symbol',  'last_updated', 'favorites'];
  dataSource = new MatTableDataSource<CoinInfo>();
  public selectedCoin: CoinInfo;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  public setFavorite(element: CoinInfo) : void {
    if(this.favoritesSet.has(element.id)) {
      this.favoritesSet.delete(element.id);
    }
    else {
      this.favoritesSet.add(element.id);
    }
    this.sharedData.coin$.next([...this.favoritesSet]);
  }

  public favoritesSet = new Set<string>();

  public setSelectedCoin(coin: CoinInfo) {
    this.selectedCoin = coin;
    this.sharedData.selectedCoin$.next(coin.id);
  }
  
  constructor(private coinService: CoinsService, private sharedData: SharedDataService) { }

  ngOnInit(): void {
    this.coinService.getCoins().subscribe((data: CoinInfo[]) => {
      this.dataSource.data = data;
    });
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }
}