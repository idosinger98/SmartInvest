import {StockChart} from "../../../static/js/stockChart.js";
import {sendChart} from "./overlayLogic";

const chart = new StockChart();

chart.loadChartFromJson(JSON.stringify(analyzeData));
chart.drawChart('chart_container');

const submitButton = document.getElementById('submitButton');

submitButton.addEventListener('click',  () => {
    submitButton.blur();
    sendChart(chart);
});