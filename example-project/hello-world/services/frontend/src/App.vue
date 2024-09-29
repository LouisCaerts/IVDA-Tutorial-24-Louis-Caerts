<template>
  <v-app>
    <v-app-bar app color="primary" dark class="pl-4">
      <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <h2 ps="5">Louis Caerts — 23-724-693</h2>
    </v-app-bar>
    <v-main>
      <ConfigurationPanel :drawer="drawer"/>
    </v-main>
  </v-app>
</template>

<style>
/* disable scrolling */
html {
  scrollbar-width: none; /* For Firefox */
  -ms-overflow-style: none; /* For Internet Explorer and Edge */
}
html::-webkit-scrollbar {
  width: 0px; /* For Chrome, Safari, and Opera */
}
</style>

<script>
import ConfigurationPanel from './components/ConfigurationPanel.vue'

export default {
  name: 'App',

  components: {
    ConfigurationPanel,
  },

  data: () => ({
    drawer: true
  }),
}
</script>
