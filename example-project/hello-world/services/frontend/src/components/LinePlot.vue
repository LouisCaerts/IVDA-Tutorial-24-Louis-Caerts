<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Profit View of {{ this.CompanyName }} (2017-2021)</h3>
    </v-row>
    <div style="height: 80vh">
      <div id='myLinePlot' style="height: inherit"></div>
    </div>
  </div>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  name: "LinePlot",
  props: ["selectedCompany", "selectedAlgorithm"],
  watch: {
   selectedCompany() {
   this.LinePlotData.x = [];
   this.LinePlotData.y = [];
   this.LinePlotData.predicted_x = [];
   this.LinePlotData.predicted_y = [];
   this.LinePlotData.category = '';

   this.fetchData();
   },
   selectedAlgorithm() {
   this.LinePlotData.x = [];
   this.LinePlotData.y = [];
   this.LinePlotData.predicted_x = [];
   this.LinePlotData.predicted_y = [];
   this.LinePlotData.category = '';

   this.fetchData();
   }
  },
  data: () => ({
    LinePlotData: {x: [], y: [], predicted_x: [], predicted_y: [], category: ''},
    CompanyName: ''
  }),
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      // req URL to retrieve single company from backend
      var reqUrl = 'http://127.0.0.1:5000/companies/' + this.$props.selectedCompany +
      '?algorithm=' + this.$props.selectedAlgorithm
      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();
      this.LinePlotData.category = responseData.category
      this.CompanyName = responseData.name
      // transform data to usable by lineplot
      responseData.profit.forEach((profit) => {
        if (profit.year <= 2021) {
          this.LinePlotData.x.push(profit.year)
          this.LinePlotData.y.push(profit.value)
        } else {
          this.LinePlotData.predicted_x.push(profit.year)
          this.LinePlotData.predicted_y.push(profit.value)
        }
      })
      // draw the lineplot after the data is transformed
      this.drawLinePlot()
    },
    drawLinePlot() {
      var colors = {
        'tech': 'blue',
        'health': 'red',
        'bank': 'green',
        'other': 'black'
      };
      var historicTrace = {
        x: this.LinePlotData.x,
        y: this.LinePlotData.y,
        type: 'scatter',
        mode: 'lines+markers',
        line: {
          color: colors[this.LinePlotData.category || 'other'],
          width: 2
        },
        marker: {
          color: colors[this.LinePlotData.category || 'other'],
          size: 10,
          symbol: 'circle'
        }
      };
      var connectingTrace = {
        x: [this.LinePlotData.x[0], this.LinePlotData.predicted_x[this.LinePlotData.predicted_x.length - 1]],  // Last point of solid and first point of dashed
        y: [this.LinePlotData.y[0], this.LinePlotData.predicted_y[this.LinePlotData.predicted_y.length - 1]],  // Corresponding y-values
        type: 'scatter',
        mode: 'lines',              // Only line, no markers
        line: {
          color: colors[this.LinePlotData.category || 'other'],
          width: 2,
          dash: 'dash'              // Set dash style for connecting line
        }
      };
      var predictedTrace = {
        x: this.LinePlotData.predicted_x,
        y: this.LinePlotData.predicted_y,
        type: 'scatter',
        line: {
          color: colors[this.LinePlotData.category || 'other'],
          width: 2,
          dash: 'dash'
        },
        marker: {
          color: colors[this.LinePlotData.category || 'other'],
          size: 10,
          symbol: 'circle-open'
        }
      }
      var data = [historicTrace, connectingTrace, predictedTrace];
      var layout = {xaxis: {title: "Year"}, yaxis: {title: "Profit (in millions)"}, margin: {t: 10, pad: 0}, showlegend: false}
      var config = {responsive: true, displayModeBar: false}
      Plotly.newPlot('myLinePlot', data, layout, config);
    }
  }
}
</script>