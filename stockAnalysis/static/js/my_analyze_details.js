import {StockChart} from "../../../static/js/stockChart.js";
import {MESSAGE_TYPE, sendToastMessage} from "../../../static/js/toastinette.js";

const chart = new StockChart();
$(document).ready(function () {
    if (document.getElementById('message')) {
        const message = document.getElementById('message').textContent;
        sendToastMessage(message, MESSAGE_TYPE.SUCCESS);
    }
});

chart.loadChartFromJson(JSON.stringify(analyzeData));
chart.drawChart('chart_container');

