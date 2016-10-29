/// <reference path="../typings/jquery.d.ts" />
/// <reference path="../typings/chart.d.ts" />

import { DashboardWebSocketTemperatureListener, theWsApi } from '../wsApi';

/**
 * TemperatureView
 */
class TemperatureView {
    chart: Chart;
    data: LineChartData;
    dataset: LineChartDataset;

    constructor() {
        let context = $("#temperatureChart");
        this.dataset = {
            label: "temperature",
            data: []
        }
        this.data = {
            labels: [],
            datasets: [this.dataset]
        }
        let config: LineChartConfig = {
            type: "line",
            data: this.data
        };
        this.chart = new Chart(context, config);
    }

    private update() {
        this.chart.update();
    }

    public addTemperature(temperature: number, time: number) {
        this.dataset.data.push(temperature);
        let d = new Date(time);
        this.data.labels.push(d.toLocaleDateString());
        this.update();
    }
}

/**
 * TemperatureController
 */
export class TemperatureController implements DashboardWebSocketTemperatureListener {

    private view: TemperatureView;

    constructor() {
        this.view = new TemperatureView();
        theWsApi.addTemperatureListener(this);
    }

    public onTemperature(temperature: number, time: number) {
        this.view.addTemperature(temperature, time);
    }
}
