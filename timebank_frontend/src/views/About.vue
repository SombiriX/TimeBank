<template>
  <v-container fluid>
    <v-layout column align-center justify-center fill-height class="about">
      <v-flex xs12>
        <div class="body-2 about_text">
          <span>Time Bank is a </span>
          <span class="confirm_selection">simple </span>
          <span>way allocate and track time for specific tasks without the tedium of attempting to schedule every second of the day</span>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<style>.confirm_selection {
    animation: glow .9s infinite alternate;
}

@keyframes glow {
    to {
        text-shadow: 0 0 10px #4caf50;
    }
}

.confirm_selection {
    font-family: sans-serif;
    font-size: 18px;
    font-weight: bold;
}

.about {
  height: 500;
}

.about_text {
  height: 100;
}
</style>
