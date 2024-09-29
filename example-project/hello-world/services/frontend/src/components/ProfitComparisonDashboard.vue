<template>
    <div>
        <v-container fluid>
            <v-row>

                <v-col cols="12" md="6">
                    <BarPlot :key="barPlotId"
                    :selectedCompany="selectedCompany"
                    :selectedAlgorithm="selectedAlgorithm"
                    @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany" />

                    <TablePlot :key="tablePlotId"
                    :selectedCompany="selectedCompany"
                    :selectedAlgorithm="selectedAlgorithm" />
                </v-col>

                <v-col cols="12" md="6">
                    <CompanyAnalysis :key="companyAnalysisId"
                    :selectedCompany="selectedCompany" />
                </v-col>

            </v-row>
        </v-container>
    </div>
</template>

<script>
import TablePlot from './TablePlot';
import BarPlot from './BarPlot';
import CompanyAnalysis from './CompanyAnalysis'

export default {
    components: {TablePlot, BarPlot, CompanyAnalysis},
    props: [
        "selectedCompany",
        "selectedAlgorithm"
    ],
    watch: {
        selectedCompany: function () {},
        selectedAlgorithm: function () {}
    },
    data: () => ({
        tablePlotId: 0,
        barPlotId: 0
    }),
    methods: {
        changeCurrentlySelectedCompany(companyId) {
            this.$emit('changeCurrentlySelectedCompany', companyId)
        },
    }
}
</script>