<template>
  <v-app dark>
    <v-content>
      <v-toolbar color="primary" dense>
        <v-toolbar-title>
          Time Bank
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn
          flat
          to="/about"
        >
          About
        </v-btn>
        <v-btn
          flat
          to="/register"
        >
          Sign Up
        </v-btn>
        <v-btn
          flat
          to="/login"
        >
          Login
        </v-btn>
        <v-btn
          flat
          to="/logout"
        >
          Logout
        </v-btn>
      </v-toolbar>
      <router-view/>
    </v-content>
    <v-footer :fixed="fixed" app>
      <span>&copy; 2018
        <a href="https://github.com/SombiriX/TimeBank">
          Sombiri Enwemeka
        </a>
      </span>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      fixed: false,
      title: 'Time Bank',
    };
  },
};
</script>
