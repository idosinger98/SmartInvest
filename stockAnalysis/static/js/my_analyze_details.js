import {StockChart} from "../../../static/js/stockChart.js";

const chart = new StockChart();

chart.loadChartFromJson(JSON.stringify(analyzeData));
chart.drawChart('chart_container');