<template>
  <div>
    <v-container>
      <v-row>
        <v-navigation-drawer permanent dark v-model="optionsOn" :location="$vuetify.display.mobile ? 'top' : undefined" :style="$vuetify.display.mobile ? 'max-height: 30%;' : ''">
          
          <v-row>
                <v-col cols="12" sm="12" class="pb-0">
                  <div class="control-panel-font">Company Overview</div>
                </v-col>
          </v-row>
          <v-row>
                <v-col cols="12" sm="12" class="py-0">
                  <v-select
                    :items="categories.values"
                    label="Select a category"
                    dense
                    v-model="categories.selectedValue"
                    @change="changeCategory"
                  ></v-select>
                </v-col>
          </v-row>

          <v-row>
                <v-col cols="12" sm="12" class="py-0">
                    <div class="control-panel-font">Profit View of Company</div>
                </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12" class="py-0">
              <v-select
                  :items="companies.values"
                  label="Select a company"
                  dense
                  v-model="companies.selectedValue"
                  @change="changeCompany"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12" class="pt-0">
              <v-select
                  :items="algorithm.values"
                  label="Select an algorithm for prediction"
                  dense
                  v-model="algorithm.selectedValue"
                  @change="changeAlgorithm"
              ></v-select>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="12" class="pt-0">
              <div class="text-center">
                <v-btn 
                  v-if="!overlay"
                  id="overlay_btn"
                  color="primary"
                  @click="overlay = !overlay"
                >
                  Generate Haiku for<br/>selected company
                </v-btn>
                <v-btn
                  v-else disabled
                  id="overlay_btn"
                  color="primary"
                >
                  Generate Haiku for<br/>selected company
                </v-btn>
              </div>

              <v-overlay v-model="haikuLoaded" class="align-center justify-center">
                  <v-card v-show="haikuLoaded" class="haiku" id="haikuP">
                    <h3 style="padding-top:10vh;">{{ this.companies.values[this.companies.selectedValue-1].title }}</h3>
                    <p>{{ this.haiku }}</p>
                  </v-card>
              </v-overlay>

            </v-col>
          </v-row>

        </v-navigation-drawer>

        <v-row>
          <v-container fluid>
            <v-row>
              <v-col cols="12" md="6">
                <ScatterPlot :key="scatterPlotId"
                      :selectedCategory="categories.selectedValue"
                      :selectedCompany="companies.selectedValue"
                      @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany"
                />
              </v-col>
              <v-col cols="12" md="6">
                <LinePlot :key="linePlotId"
                  :selectedCompany="companies.selectedValue"
                  :selectedAlgorithm="algorithm.selectedValue"/>
              </v-col>
            </v-row>
          </v-container>

          <v-divider></v-divider>
          
          <v-container fluid>
            <v-col>
              <ProfitComparisonDashboard :key="profitComparisonDashboardId"
                :selectedCompany="companies.selectedValue"
                :selectedCategory="categories.selectedValue"
                :selectedAlgorithm="algorithm.selectedValue"
                @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany" 
              />
            </v-col>
          </v-container>

          <v-divider></v-divider>
          
        </v-row>


      </v-row>
    </v-container>
  </div>
</template>

<script>
import ScatterPlot from './ScatterPlot';
import LinePlot from './LinePlot';
import ProfitComparisonDashboard from './ProfitComparisonDashboard';

export default {
  components: {ScatterPlot, LinePlot, ProfitComparisonDashboard},
  props: [
      "drawer"
  ],
  watch: {
      drawer: function () {this.optionsOn = this.drawer;},
      overlay(val) {
        if (val) {
          this.fetchHaiku();
        }
        else {
          this.haiku = ''
          this.haikuLoaded = false
        }
      },
      haikuLoaded(val) {
        if (val) {
          this.overlay = true
        }
        else {
          this.overlay = false;
        }
      }
  },
  data: () => ({
    haiku: '',
    haikuLoaded: false,
    optionsOn: true,
    overlay: false,
    scatterPlotId: 0,
    linePlotId: 0,
    profitComparisonDashboardId: 0,
    categories: {
      values: ['All', 'tech', 'health', 'bank'],
      selectedValue: 'All'
    },
    companies: {
      values: [],
      selectedValue: 1
    },
    algorithm: {
      values: ['none', 'random', 'regression'],
      selectedValue: 'none'
    }
  }),
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      var reqUrl = 'http://127.0.0.1:5000/companies?category=All';
      const response = await fetch(reqUrl)
      const responseData = await response.json();
      responseData.forEach((company) => {
        const newCompany = {"value":company.id, "title":company.name};
        this.companies.values.push(newCompany);
      })
    },
    async fetchHaiku() {
      var reqUrl = 'http://localhost:5000/llm/groq/poem/' + this.companies.selectedValue;
      const response = await fetch(reqUrl)
      const responseData = await response.json();
      this.haiku = responseData["poem"]
      this.haikuLoaded = true;
    },
    changeCategory() {
          this.scatterPlotId += 1
        },
    changeCompany() {
          this.scatterPlotId += 1
          this.linePlotId += 1
          this.profitComparisonDashboardId += 1
    },
    changeAlgorithm() {
          this.linePlotId += 1
    },
    changeCurrentlySelectedCompany(companyId) {
      this.companies.selectedValue = companyId
      this.changeCompany()
    },
  }
}
</script>

<style scoped>
.control-panel-font {
  font-family: "Open Sans", verdana, arial, sans-serif;
  align-items: center;
  font-size: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  font-weight: 500;
  height: 40px;
  padding-left: 5px;
}
.sideBar {
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  background: #fafafa;
  padding-left: 17px;
  height: calc(100vh - 50px);
}
::v-deep ::-webkit-scrollbar {
  width: 0;
  background: transparent;
}
.haiku {
  color: white;
  text-align: center;
  font-size: 20px;
  background-color: rgba(50, 50, 50, 0.9);
  border-radius: 15px;
  white-space: pre-line;
}
.haiku p {
  padding-top: 10vh;
  padding-bottom: 10vh;
  padding-left: 10vw;
  padding-right: 10vw;
}
</style>
