/// <reference path="../typings/webcomponents.d.ts" />
/// <reference path="../typings/require.d.ts" />

import { DashboardWebSocketTemperatureListener, theWsApi } from "../wsApi";
import { MyLineChart } from "./dashboardChart";

class TemperatureChartElement extends HTMLDivElement {
    private chart: MyLineChart;
    private controller: TemperatureController;

    constructor() {
        super();
    }

    public add(temperature: number, time: string) {
        this.chart.add(temperature, time);
    }

    protected createdCallback(): void {
        console.log("TemperatureChartElement.createdCallback()");
        let canvas = document.createElement("canvas");
        canvas.width = 600;
        canvas.height = 400;
        this.appendChild(canvas);
        this.chart = new MyLineChart(canvas, this.title);
        this.controller = new TemperatureController(this);
    }
}

/**
 * TemperatureController
 */
class TemperatureController implements DashboardWebSocketTemperatureListener {

    private view: TemperatureChartElement;

    constructor(chartElement: TemperatureChartElement) {
        this.view = chartElement;
        theWsApi.addTemperatureListener(this);
    }

    public onTemperature(temperature: number, time: number) {
        let d = new Date(time);
        this.view.add(temperature, d.toTimeString());
    }
}

export function registerTemperatureChartElement() {
    document.registerElement("dashboard-temperature", TemperatureChartElement);
}
