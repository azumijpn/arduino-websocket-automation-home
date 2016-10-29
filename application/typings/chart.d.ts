// Type definitions for Chart.js
// Project: https://github.com/nnnick/Chart.js

interface LineChartDataset {
    label: string;
    data: number[];
}

interface LineChartData {
    labels: string[];
    datasets: LineChartDataset[];
}

interface ChartConfig {
    type: string;
}

interface LineChartConfig extends ChartConfig {
    type: "line";
    data: LineChartData;
}


interface Chart {
    update(): void;
}

declare var Chart: {
    new (context: any, config: ChartConfig): Chart;
};
