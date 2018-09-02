<template>
  <div id="register-view">
    <template v-if="registrationLoading">
      loading...
    </template>
    <template v-else-if="!registrationCompleted">
      <v-layout row justify-center>
        <v-card>
          <v-card-title>
            <span class="headline">Create Account</span>
          </v-card-title>
          <v-container grid-list-xs>
            <v-form
              ref="registerForm"
              @submit.prevent="submit()"
            >
              <v-text-field
                label="Email"
                :rules="[rules.required]"
                required
                v-model="inputs.email"
              >
              </v-text-field>
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
                v-model="inputs.password1"
              >
              </v-text-field>
              <v-text-field
                name="name"
                label="Confirm Password"
                min="8"
                :append-icon="pwd_visibility ? 'visibility' : 'visibility_off'"
                @click:append="() => (pwd_visibility = !pwd_visibility)"
                value="Password"
                :rules="[rules.required, rules.atLeast8, rules.passMatch]"
                :type="pwd_visibility ? 'text' : 'password'"
                v-model="inputs.password2"
              >
              </v-text-field>
              <v-container grid-list-md text-xs-center>
                <v-layout row align-center justify-center>
                  <v-btn flat type='submit'>create account</v-btn>
                </v-layout>
                <v-layout row>
                  <v-flex xs14>
                    <v-alert
                    type="error"
                    dismissible
                    :value="registrationError"
                    transition="fade-transition"
                    >
                     An error occured while processing your request.
                    </v-alert>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-card-actions>
                    <v-flex>
                      Already have an account?
                    </v-flex>
                    <v-flex>
                      <router-link to="/login">login</router-link>
                    </v-flex>
                    <v-flex>
                      <router-link to="/password_reset">
                        reset password
                      </router-link>
                    </v-flex>
                  </v-card-actions>
                </v-layout>
              </v-container>
            </v-form>
          </v-container>
        </v-card>
      </v-layout>
    </template>
    <template v-else>
      <div>
        Registration complete. You should receive an email shortly with
        instructions on how to activate your account.
      </div>
      <div>
        <v-btn to="/login">return to login page</v-btn>
      </div>
    </template>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  data () {
    return {
      inputs: {
        username: '',
        password1: '',
        password2: '',
        email: ''
      },
      pwd_visibility: false,
      rules: {
        required: value => value.length > 0 || 'This field is required',
        atLeast8: value => (
          value.length >= 8 || 'At least 8 characters required'
        ),
        passMatch: value => (
          value === this.inputs.password1 || 'Passwords do not match'
        )
      }
    }
  },
  computed: mapState('signup', [
    'registrationCompleted',
    'registrationError',
    'registrationLoading'
  ]),
  methods: Object.assign({},
    mapActions('signup', [
      'createAccount',
      'clearRegistrationStatus'
    ]),
    {
      submit: function () {
        // Validate inputs and login
        if (this.$refs.registerForm.validate()) {
          var inputs = this.inputs
          this.createAccount(inputs)
        }
      }
    }
  ),
  beforeRouteLeave: function (to, from, next) {
    this.clearRegistrationStatus()
    next()
  }
}
</script>
