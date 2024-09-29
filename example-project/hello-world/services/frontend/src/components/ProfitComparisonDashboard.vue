<template>
    <div>
        <v-container fluid>
            <v-row>

                <v-col>
                    <TablePlot :key="tablePlotId"
                    :selectedCompany="selectedCompany"
                    :selectedAlgorithm="selectedAlgorithm" />
                </v-col>

                <v-col>
                    <BarPlot :key="barPlotId"
                    :selectedCompany="selectedCompany"
                    :selectedAlgorithm="selectedAlgorithm"
                    @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany" />
                </v-col>

            </v-row>
        </v-container>
    </div>
</template>

<script>
import TablePlot from './TablePlot';
import BarPlot from './BarPlot';

export default {
    components: {TablePlot, BarPlot},
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