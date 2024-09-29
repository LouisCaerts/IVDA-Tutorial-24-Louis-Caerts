<template>
    <div>
        <v-row align="center" justify="center" class="mt-1 mb-0">
            <h3>{{ this.Category }} companies' average yearly profit (excluding predictions)</h3>
        </v-row>
        <div style="max-height: 80vh">
            <div id='myBarPlot' style="height: inherit"></div>
        </div>
    </div>
</template>

<script>
    import Plotly from 'plotly.js/dist/plotly';
    
    export default {
        name: "BarPlot",
        props: [
            "selectedCompany"
        ],
        watch: {
            selectedCompany: function () {
                this.BarPlotData.x = [];
                this.BarPlotData.y = [];
                this.BarPlotData.sorted_x = [];
                this.BarPlotData.sorted_y = [];
                this.BarPlotData.companyId = [];
                this.BarPlotData.sorted_companyId = [];
                this.Category = '';
                this.SelectedCompanyName = '';

                this.fetchData();
            }
        },
        data: () => ({
            BarPlotData: {x: [], y: [], sorted_x: [], sorted_y: [], companyId: [], sorted_companyId: []},
            Category: '',
            SelectedCompanyName: ''
        }),
        mounted() {
            this.fetchData()
        },
        methods: {
            async fetchData() {
                var reqUrl1 = 'http://127.0.0.1:5000/companies/' + this.$props.selectedCompany + '?algorithm=none'
                const response1 = await fetch(reqUrl1)
                const responseData1 = await response1.json();

                this.Category = responseData1.category;
                this.SelectedCompanyName = responseData1.name;

                var reqUrl2 = 'http://127.0.0.1:5000/companies?category=' + this.Category
                const response2 = await fetch(reqUrl2)
                const responseData2 = await response2.json();
                
                var companyProfits;
                responseData2.forEach((company) => {
                    this.BarPlotData.companyId.push(company.id);
                    this.BarPlotData.x.push(company.name)
                    companyProfits = []
                    company.profit.forEach((profit) => {
                        companyProfits.push(profit.value);
                    })
                    this.BarPlotData.y.push((companyProfits.reduce((acc, val) => acc + val, 0)) / company.profit.length)
                })

                // Sorting data, descending
                var sortedData = this.BarPlotData.x.map((name, index) => ({
                    name: name,
                    profit: this.BarPlotData.y[index],
                    id: this.BarPlotData.companyId[index]
                }));

                sortedData.sort((a, b) => b.profit - a.profit);

                this.BarPlotData.sorted_x = sortedData.map(item => item.name);
                this.BarPlotData.sorted_y = sortedData.map(item => item.profit);
                this.BarPlotData.sorted_companyId = sortedData.map(item => item.id);

                this.drawBarPlot()
            },
            drawBarPlot() {
                var colors = {
                    'tech': 'blue',
                    'health': 'red',
                    'bank': 'green',
                    'other': 'black'
                };
                var mutedColors = {
                    'tech': 'rgba(0, 0, 255, 0.6)', // blue
                    'health': 'rgba(255, 0, 0, 0.6)', // red
                    'bank': 'rgba(0, 128, 0, 0.6)', // green
                    'other': 'rgba(0, 0, 0, 0.6)' // black
                };
                var barColors = Array(this.BarPlotData.x.length).fill(mutedColors[this.Category || 'other']);
                barColors[this.BarPlotData.sorted_x.indexOf(this.SelectedCompanyName)] = colors[this.Category || 'other'];
                var data = [{
                    type: 'bar',
                    width: 0.6,
                    companyId: this.BarPlotData.sorted_companyId,
                    x: this.BarPlotData.sorted_x,
                    y: this.BarPlotData.sorted_y,
                    marker: {
                        color: barColors
                    }
                }];
                var layout = {xaxis: {title: "Company name", tickangle: -30}, yaxis: {title: "Average profit (2017-2021)"}, margin: {t: 10, pad: 0}}
                var config = {responsive: true, displayModeBar: false}
                Plotly.newPlot('myBarPlot', data, layout, config);
                this.clickBarPlot()
            },
            clickBarPlot() {
                var that = this
                var myPlot = document.getElementById('myBarPlot')
                myPlot.on('plotly_click', function (data) {

                    var pn = '';

                    for (var i = 0; i < data.points.length; i++) {

                        // get the index of clicked point
                        pn = data.points[i].pointNumber;

                        // emit event to change the currently selected company in the a) configuration panel
                        // and b) update the Profit View
                        that.$emit('changeCurrentlySelectedCompany', data.points[i].data.companyId[pn])
                    }
                })
            }
        }
    }
</script>