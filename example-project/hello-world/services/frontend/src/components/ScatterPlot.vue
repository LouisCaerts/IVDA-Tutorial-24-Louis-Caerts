<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Overview of {{ $props.selectedCategory }} Companies</h3>
    </v-row>
    <div style="height: 80vh">
      <div id='myScatterPlot' style="height: inherit"></div>
    </div>
  </div>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly';

export default {
  name: "ScatterPlot",
  props: [
    "selectedCategory",
    "selectedCompany"
  ],
  watch: {
   selectedCategory: function () {
    this.ScatterPlotData.x = [];
    this.ScatterPlotData.y = [];
    this.ScatterPlotData.name = [];
    this.ScatterPlotData.category = [];
    this.ScatterPlotData.symbol = [];
    this.ScatterPlotData.companyId = [];

    this.fetchData();
   },
   selectedCompany: function () {
    this.ScatterPlotData.x = [];
    this.ScatterPlotData.y = [];
    this.ScatterPlotData.name = [];
    this.ScatterPlotData.category = [];
    this.ScatterPlotData.symbol = [];
    this.ScatterPlotData.companyId = [];

    this.fetchData();
   }
   },
  data: () => ({
    ScatterPlotData: {x: [], y: [], name: [], category: [], symbol: [], companyId: []},
  }),
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.$props.selectedCategory
      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();

      // transform data to usable by scatterplot
      responseData.forEach((company) => {
        this.ScatterPlotData.name.push(company.name)
        this.ScatterPlotData.category.push(company.category)
        this.ScatterPlotData.x.push(company.founding_year)
        this.ScatterPlotData.y.push(company.employees)
        this.ScatterPlotData.symbol.push(company.id === this.$props.selectedCompany ? 'x' : 'circle');
        this.ScatterPlotData.companyId.push(company.id)
      })
      // after the data is loaded, draw the plot
      this.drawScatterPlot()
    },
    drawScatterPlot() {
      var colors = {
        'tech': 'blue',
        'health': 'red',
        'bank': 'green',
        'other': 'black'
      };
      var trace1 = {
        x: this.ScatterPlotData.x,
        y: this.ScatterPlotData.y,
        mode: 'markers',
        type: 'scatter',
        text: this.ScatterPlotData.name,
        companyId: this.ScatterPlotData.companyId,
        marker: {
          symbol: this.ScatterPlotData.symbol,
          color: this.ScatterPlotData.category.map(cat => colors[cat] || colors['other']),
          size: 10
        }
      };
      var data = [trace1];
      var layout = {xaxis: {title: "Founding year"}, yaxis: {title: "# of employees"}, margin: {t: 10, pad: 0}}
      var config = {responsive: true, displayModeBar: false}
      Plotly.newPlot('myScatterPlot', data, layout, config);
      this.clickScatterPlot()
    },
    clickScatterPlot() {
      var that = this
      var myPlot = document.getElementById('myScatterPlot')
      myPlot.on('plotly_click', function (data) {

        var pn = '';
        var colors = [];
        var symbols = [];

        for (var i = 0; i < data.points.length; i++) {

          // get the index of clicked point
          pn = data.points[i].pointNumber;

          // emit event to change the currently selected company in the a) configuration panel
          // and b) update the Profit View
          that.$emit('changeCurrentlySelectedCompany', data.points[i].data.companyId[pn])

          // maintain all colors
          colors = data.points[i].data.marker.color;

          // revert all symbols
          symbols = data.points[i].data.marker.symbol;
          symbols.fill('circle');

          // and change currently selected symbol to an X
          symbols[pn] = 'x';

          // update the marker and plot
          var update = {'marker': {symbol: symbols, color: colors, size: 10}};

          // Update the plot
          Plotly.restyle('myScatterPlot', update);
        }
      });
    }
  }
}
</script>