import { ChartData } from './../../models/ChartData';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { CoinsService } from './../../services/coins.service';
import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { switchMap } from 'rxjs';
import { EChartsOption } from 'echarts';

@Component({
  selector: 'app-graphic',
  templateUrl: './graphic.component.html',
  styleUrls: ['./graphic.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GraphicComponent implements OnInit {

  public hours: string[] = [];
  public coinValues: number[] = [];
  public updateOptions: any;

  public options: any = {
    legend: {
      data: ['bar'],
      align: 'left',
    },
    tooltip: {},
    xAxis: {
      data: this.hours,
      silent: false,
      splitLine: {
        show: false,
      },
    },
    yAxis: {},
    series: [
      {
        name: 'bar',
        type: 'bar',
        data: this.coinValues,
        animationDelay: (idx: number) => idx * 10,
      },
    ],
    animationEasing: 'elasticOut',
    animationDelayUpdate: (idx: number) => idx * 5,
  };

  constructor(
    private sharedData: SharedDataService,
    private coinService: CoinsService,
    private cdr: ChangeDetectorRef) { }

  ngOnInit(): void {
    this.sharedData
      .getSelectedCoin()
      .pipe(switchMap(coinId => {
        return this.coinService.getHistoryDataForCoin(coinId)
      })).subscribe((chartData: ChartData) => {
          this.formatChartData(chartData);
          this.updateOptions = {
            xAxis: {
              data: this.hours
            },
            yAxis: {
              scale: true
            },
            series: [{
              data: this.coinValues
            }]
          };
      });
  }

  private formatChartData(chartData: ChartData) {
    this.hours = [];
    this.coinValues = [];

    for(let i=0; i<chartData.prices.length;i++) {
      const price = chartData.prices[i];
      const priceTime =  new Date(price[0]);
      const value = price[1].toFixed(2);

      this.hours.push(priceTime.toLocaleString());
      this.coinValues.push(+value);
    }

    this.cdr.markForCheck();
  }
}