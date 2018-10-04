<template>
  <v-container fluid>
    <v-layout column align-center class="display-4">
      <v-flex xs1>
        <transition name="slide">
          <span>Simple.</span>
        </transition>
      </v-flex>
      <v-flex xs1>
        Efficient.
      </v-flex>
      <v-flex xs1>
        Time Tracking.
      </v-flex>
    </v-layout>
  </v-container>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
