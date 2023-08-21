import {IndicatorCheckBox} from "./indicatorCheckBox.js";
import { STOCK_KEYS, COLORS, CHART_JSON_KEYS} from "./constants.js";


export class StockChart {

    constructor() {
        this.chart = anychart.stock();
        this.indicator_to_plot_map = {};
        this.indicators_checkboxes = [];
        this.data = {};
    }

    createFromData(data) {
        let stockData;
        let volumeData;

        [stockData,volumeData] = this.formatDataToChartApi(data);
        const plot = this.chart.plot(0);
        this.setupGraphSettings(plot, stockData);
        this.setupStockVolumeSettings(plot, volumeData);
        this.data = data;
    }

    setupGraphSettings(plot,data){
        plot.yGrid(true).xGrid(true).yMinorGrid(true).xMinorGrid(true);
        const series = plot.candlestick(data);
        series.name('stock name');
        series.risingFill(COLORS.GREEN);
        series.fallingFill(COLORS.RED);
        series.risingStroke(COLORS.GREEN);
        series.fallingStroke(COLORS.RED);
        // make scroller and the details line invisible
        this.showScroller(false);
        plot.legend().enabled(false);
    }

    setupStockVolumeSettings(plot, data){
        const volumeSeries = plot.column(data);
        // set series settings
        volumeSeries.name(STOCK_KEYS.VOLUME).zIndex(100).maxHeight('15%').bottom(0); // maybe remove the zindex

        // create a logarithmic scale
        const customScale = anychart.scales.log();
        // sets y-scale
        volumeSeries.yScale(customScale);
        volumeSeries.risingStroke(COLORS.RED);
        volumeSeries.fallingStroke(COLORS.GREEN);
        volumeSeries.risingFill(COLORS.RED + ' 0.7');
        volumeSeries.fallingFill(COLORS.GREEN + ' 0.7');
    }

    showScroller(enable){
        this.chart.scroller().enabled(enable);
    }

    drawChart(container) {
        anychart.onDocumentReady(() => {
            this.chart.container(container);
            this.chart.draw();

            const rangeSelector = anychart.ui.rangeSelector().render(this.chart);
        });
    }

    async chartToJson(){
        const chartData = {};

        chartData[CHART_JSON_KEYS.DATA] = this.data;
        chartData[CHART_JSON_KEYS.INDICATORS] = [];
        chartData[CHART_JSON_KEYS.ANNOTATIONS] = null;
        chartData['image'] = (await this.chartToPng());
        this.indicators_checkboxes
            .filter(indicator => indicator.isChecked())
            .forEach(indicator => chartData[CHART_JSON_KEYS.INDICATORS].push(indicator.getElementData()));

        return JSON.stringify(chartData);
    }

    loadChartFromJson(json){
        const jsonData = JSON.parse(json);

        this.createFromData(jsonData[CHART_JSON_KEYS.DATA]);
        jsonData[CHART_JSON_KEYS.INDICATORS].forEach(data => this.addIndicatorToChart(data));
    }

    chartToPng() {
        return new Promise((resolve, reject) => {
            anychart.onDocumentReady(() => {
                this.chart.getPngBase64String(response => {
                    const dataURL = `data:image/png;base64, ${response}`;
                    resolve(dataURL); // Resolve the Promise with the dataURL
                });
            });
        });
    }

    addIndicatorToChart(data) {
        for (const key of Object.keys(data)) {
            this.addIndicatorLineSeriesOnNewPlot(data[key], key);
            // for now everyone is on new plot.
        }
    }

    addIndicatorLineSeriesOnNewPlot(data, indicatorName, color) {
        const plotIndex = this.chart.getPlotsCount() + 1;
        const plot = this.chart.plot(plotIndex);

        plot.title(indicatorName);
        this.indicator_to_plot_map[indicatorName] = plotIndex;
        for(const key in data){
            this.addLineSeriesOnPlot(data[key], plot, key, color);
        }
    }

    addLineSeriesOnPlot(data, plot, name, color) {
        const lineSeries = plot.line(data);

        lineSeries.stroke(color);
        lineSeries.name(name);
        lineSeries.id(name);
    }

    removeIndicatorLine(name){
        const plot_index = this.indicator_to_plot_map[name];

        if(plot_index !== 0){
            this.chart.plot(plot_index).remove();
            this.chart.plot(plot_index).enabled(false);
        }
        else{
            this.chart.plot(plot_index).removeSeries(name);
        }
    }

    addIndicatorCheckBox(indicatorCheckBox, data){
        this.indicators_checkboxes.push(indicatorCheckBox);
        indicatorCheckBox.addStatusChangeEventListener(
            (data)=> indicatorCheckBox.getIndicatorAsync(data, this),
            (name)=> this.removeIndicatorLine(name),
            data
        );
    }

    formatDataToChartApi(data){
        const volumeData = [];
        const newData = [];

        for (const timestamp of Object.keys(data.Open)) {
            newData.push([
                parseInt(timestamp),
                data[STOCK_KEYS.OPEN][timestamp],
                data[STOCK_KEYS.HIGH][timestamp],
                data[STOCK_KEYS.LOW][timestamp],
                data[STOCK_KEYS.CLOSE][timestamp],
            ]);
            volumeData.push([parseInt(timestamp), data[STOCK_KEYS.VOLUME][timestamp]]);
        }

        return [newData, volumeData];
    }

    // addIndicatorLineSeriesOnMainPlot(data, indicatorName, color) {
    //     this.addIndicatorLineOnPlot(data,this.chart.plot(0),indicatorName, color);
    // }
    //
    // addAreaToPlot(data){
    //     const areaSeries = this.chart.plot(0).area(data);
    //     areaSeries.fill('rgba(255, 0, 0, 0.3)');
    // }
}