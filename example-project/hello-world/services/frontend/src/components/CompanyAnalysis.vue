<template>
    <v-container justify="center" align="center">
        <h3 class="mt-1">{{ this.CompanyName }} profit analysis</h3>
        <v-col cols="12" justify="center" align="center">
            <div>
                <v-card class="py-0 px-4">
                    <v-container v-if="!activated">
                        <p>Curious as to what factors contributed to your selected company's profits over the past few years?</p>
                        <p>Groq is an LLM that can help you with that!</p>
                        <br />
                        <p>This AI analysis is <br/><element style='color:red;font-weight:bold;'> not guaranteed to be 100% accurate</element></p>
                        <br />
                        <v-btn
                        id="analysis_btn"
                        color="primary"
                        @click="activated = !activated"
                        >
                            Generate profit analysis
                        </v-btn>
                    </v-container>
                    <v-container v-else>
                        <div id='myCompanyAnalysis' v-html="analysis"></div>
                    </v-container>
                </v-card>
            </div>
        </v-col>
    </v-container>
</template>

<script>
    export default {
        name: "TablePlot",
        props: [
            "selectedCompany"
        ],
        watch: {
            selectedCompany: function () {
                this.companyName = '';
                this.activated = false;
                this.analysis = '';

                this.fetchData();
                this.fetchAnalysis();
            }
        },
        data: () => ({
            CompanyName: '',
            activated: false,
            analysis: ''
        }),
        mounted() {
            this.fetchData();
            this.fetchAnalysis();
        },
        methods: {
            async fetchData() {
                var reqUrl1 = 'http://127.0.0.1:5000/companies/' + this.$props.selectedCompany + '?algorithm=' + this.$props.selectedAlgorithm;
                const response1 = await fetch(reqUrl1);
                const responseData1 = await response1.json();

                this.CompanyName = responseData1.name;
            },
            async fetchAnalysis() {
                var reqUrl2 = 'http://127.0.0.1:5000/llm/groq/analysis/' + this.$props.selectedCompany;
                const response2 = await fetch(reqUrl2);
                const responseData2 = await response2.json();

                this.analysis = responseData2.analysis;
            }
        }
    }
</script>