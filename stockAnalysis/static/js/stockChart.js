
export class StockChart {

    constructor() {
        this.chart = anychart.stock();
        this.indicator_to_plot_map = {};
    }

    createFromData(data, volumeData) {
        // create stock chart
        // create first plot on the chart
        const plot = this.chart.plot(0);
        this.setupGraphSettings(plot, data);
        this.setupStockVolumeSettings(plot, volumeData);

    }

    setupGraphSettings(plot,data){
        plot.yGrid(true).xGrid(true).yMinorGrid(true).xMinorGrid(true);
        const series = plot.candlestick(data);
        series.name('stock name');
        series.legendItem().iconType('rising-falling');
        series.risingFill('green');
        series.fallingFill('red');
        series.risingStroke('green');
        series.fallingStroke('red');
        // make scroller and the details line invisible
        this.showScroller(false);
        plot.legend().enabled(false);
    }

    setupStockVolumeSettings(plot, data){
        // create volume series on the plot
        const volumeSeries = plot.column(data);
        // set series settings
        volumeSeries.name('Volume').zIndex(100).maxHeight('15%').bottom(0); // maybe remove the zindex

        // create a logarithmic scale
        const customScale = anychart.scales.log();
        // sets y-scale
        volumeSeries.yScale(customScale);

        // set volume rising and falling stroke and fill settings
        volumeSeries.risingStroke('red');
        volumeSeries.fallingStroke('green');
        volumeSeries.risingFill('red 0.7');
        volumeSeries.fallingFill('green 0.7');
    }

    showScroller(enable){
        this.chart.scroller().enabled(enable);
    }

    drawChart(container) {
        anychart.onDocumentReady(() => {
            // set container id for the chart and draw
            this.chart.container(container);
            this.chart.draw();

            // create and init range selector
            const rangeSelector = anychart.ui.rangeSelector().render(this.chart);
        });
    }

    saveChart(){
        return this.chart.toJson();
    }

    // loadChartFromJson(json){
    //     this.chart = anychart.fromJson(json);
    // }

    addIndicatorLineOnNewPlot(data, indicatorName, color) {
        const plotIndex = this.chart.getPlotsCount() + 1;
        const plot = this.chart.plot(plotIndex);
        this.indicator_to_plot_map[indicatorName] = plotIndex;

        this.addIndicatorLineOnPlot(data,plot,indicatorName, color);
    }

    addIndicatorLineOnMainPlot(data, indicatorName, color) {
        this.addIndicatorLineOnPlot(data,this.chart.plot(0),indicatorName, color);
    }

    addIndicatorLineOnPlot(data,plot, name, color) {
        const lineSeries = plot.line(data);

        // Customize the line series appearance (optional)
        lineSeries.stroke(color);
        lineSeries.name(name);
        lineSeries.id(name);
    }

    removeIndicatorLine(name){
        const plot_index = this.indicator_to_plot_map[name];

        this.chart.plot(plot_index).removeSeries(name);
        if(plot_index !== 0){
            this.chart.plot(plot_index).remove();
            this.chart.plot(plot_index).enabled(false);
        }
    }
}