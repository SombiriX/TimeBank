<template>
  <v-app dark>
    <v-content>
      <v-toolbar color="primary" dense>
        <v-card to="/home" color="primary" flat>
          <v-toolbar-title>
            Time Bank
          </v-toolbar-title>
        </v-card>
        <v-spacer></v-spacer>
        <v-btn
          flat
          to="/about"
        >
          About
        </v-btn>
        <v-btn v-if="!isAuthenticated" flat to="/register">Sign Up</v-btn>
        <v-btn v-if="isAuthenticated" flat to="/logout">Logout</v-btn>
        <v-btn v-else flat to="/login">Login</v-btn>
        <v-btn v-if="isAuthenticated" flat to="/timebank">Goto Time Bank</v-btn>
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
  data () {
    return {
      fixed: false,
      title: 'Time Bank'
    }
  },
  computed: {
    isAuthenticated: function () {
      return this.$store.getters['auth/isAuthenticated']
    }
  }
}
</script>
