<template>
    <div>
        <v-row text-align="center" justify="center" class="mt-2 mb-0">
            <h3>{{ this.CompanyName }} yearly profits</h3>
        </v-row>
        <div>
            <div style="height: 250px;" id='myTablePlot'></div>
        </div>
    </div>
</template>

<script>
    import Plotly from 'plotly.js/dist/plotly';

    export default {
        name: "TablePlot",
        props: [
            "selectedCompany",
            "selectedAlgorithm"
        ],
        watch: {
            selectedCompany: function () {
                this.TablePlotData.years = [];
                this.TablePlotData.profits = [];
                this.companyName = '';
                this.TablePlotData.category = [];

                this.fetchData();
            },
            selectedAlgorithm: function () {
                this.TablePlotData.years = [];
                this.TablePlotData.profits = [];
                this.companyName = '';
                this.TablePlotData.category = [];

                this.fetchData();
            }
        },
        data: () => ({
            TablePlotData: {years: [], profits: [], category: []},
            CompanyName: ''
        }),
        mounted() {
            this.fetchData()
        },
        methods: {
            async fetchData() {
                var reqUrl = 'http://127.0.0.1:5000/companies/' + this.$props.selectedCompany + '?algorithm=' + this.$props.selectedAlgorithm
                const response = await fetch(reqUrl)
                const responseData = await response.json();

                this.TablePlotData.category = responseData.category
                this.CompanyName = responseData.name
                
                responseData.profit.forEach((profit) => {
                    this.TablePlotData.years.push(profit.year)
                    this.TablePlotData.profits.push(Math.round(profit.value))
                })

                var editedYears = []
                this.TablePlotData.years.forEach((year) => {
                    if (year <= 2021) editedYears.push((year));
                    else editedYears.push((year) + ' (predicted)');
                })
                this.TablePlotData.years = editedYears;

                this.drawTablePlot()
            },
            drawTablePlot() {
                var colors = {
                    'tech': 'blue',
                    'health': 'red',
                    'bank': 'green',
                    'other': 'black'
                };
                var values = [
                    this.TablePlotData.years.reverse(),
                    this.TablePlotData.profits.reverse()
                ];
                var data = [{
                    type: 'table',
                    header: {
                        values: [["<b>YEAR</b>"], ["<b>PROFIT (IN MILLIONS)</b>"]],
                        align: "center",
                        line: {width: 1, color: 'black'},
                        fill: {color: colors[this.TablePlotData.category || 'other']},
                        font: {family: "Arial", size: 12, color: "white"},
                        valign: "center"
                    },
                    cells: {
                        values: values,
                        align: "center",
                        line: {color: "black", width: 1},
                        font: {family: "Arial", size: 11, color: ["black"]}
                    }
                }];
                var layout = {margin: {t: 10, pad: 0}, autosize: true,}
                var config = {responsive: true, displayModeBar: false}
                Plotly.newPlot('myTablePlot', data, layout, config);
            },
        }
    }
</script>