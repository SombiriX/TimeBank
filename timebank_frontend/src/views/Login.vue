<template>
  <div id="login-view">
    <v-layout row justify-center>
      <v-form
        ref="loginForm"
        @submit.prevent="submit()"
      >
        <v-card round>
          <v-container grid-list-xs>
            <v-text-field
              label="Username"
              :rules="[rules.required]"
              required
              v-model="inputs.username"
            >
            </v-text-field>
            <v-text-field
              name="name"
              label="Password"
              min="8"
              :append-icon="pwd_visibility ? 'visibility' : 'visibility_off'"
              @click:append="() => (pwd_visibility = !pwd_visibility)"
              value="Password"
              :rules="[rules.required, rules.atLeast8]"
              :type="pwd_visibility ? 'text' : 'password'"
              v-model="inputs.password"
            >
            </v-text-field>
          </v-container>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn to="/register">create account</v-btn>
            <v-btn to="/password_reset">reset password</v-btn>
            <v-btn
              id="login-button"
              type="submit"
            >
              login
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-layout>
  </div>
</template>

<script>
export default {
  data () {
    return {
      inputs: {
        username: '',
        password: ''
      },
      pwd_visibility: false,
      rules: {
        required: value => value.length > 0 || 'This field is required',
        atLeast8: value => value.length >= 8 || 'At least 8 chracters required'
      }
    }
  },
  methods: {
    login: function () {
      // Get user input
      var username = this.inputs.username
      var password = this.inputs.password

      // Call vuex login action
      this.$store.dispatch('auth/login', { username, password })
        .then(() => this.$router.push('/'))
    },
    submit: function () {
      // Validate inputs and login
      if (this.$refs.loginForm.validate()) {
        this.login()
      }
    }
  }
}
</script>
