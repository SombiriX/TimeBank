<template>
  <div id="register-view">
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
              required
              v-model="inputs.email"
              @input="$v.inputs.email.$touch()"
              @blur="$v.inputs.email.$touch()"
              :error-messages="emailErrors"
            >
            </v-text-field>
            <v-text-field
              label="Username"
              required
              v-model="inputs.username"
              @input="$v.inputs.username.$touch()"
              @blur="$v.inputs.username.$touch()"
              :error-messages="usernameErrors"
            >
            </v-text-field>
            <v-text-field
              name="name"
              label="Password"
              min="8"
              :append-icon="pwd_visibility ? 'visibility' : 'visibility_off'"
              @click:append="() => (pwd_visibility = !pwd_visibility)"
              value="Password"
              :type="pwd_visibility ? 'text' : 'password'"
              v-model="inputs.password1"
              @input="$v.inputs.password1.$touch()"
              @blur="$v.inputs.password1.$touch()"
              :error-messages="pass1Errors"
            >
            </v-text-field>
            <v-text-field
              name="name"
              label="Confirm Password"
              min="8"
              :append-icon="pwd_visibility ? 'visibility' : 'visibility_off'"
              @click:append="() => (pwd_visibility = !pwd_visibility)"
              value="Password"
              :type="pwd_visibility ? 'text' : 'password'"
              v-model="inputs.password2"
              @input="$v.inputs.password2.$touch()"
              @blur="$v.inputs.password2.$touch()"
              :error-messages="pass2Errors"
            >
            </v-text-field>
            <v-container grid-list-md text-xs-center>
              <v-layout row align-center justify-center>
                <v-btn
                  flat
                  type='submit'
                  ref="createAccBtn"
                >
                  create account
                </v-btn>
              </v-layout>
              <v-layout row>
                <v-flex xs4>
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
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, maxLength, minLength, email } from 'vuelidate/lib/validators'

import { mapActions, mapState } from 'vuex'

export default {
  mixins: [validationMixin],
  data () {
    return {
      inputs: {
        username: '',
        password1: '',
        password2: '',
        email: ''
      },
      pwd_visibility: false
    }
  },
  validations: {
    inputs: {
      username: { required, maxLength: maxLength(100) },
      password1: { required, minLength: minLength(8) },
      password2: { required, minLength: minLength(8) },
      email: { required, email }
    }
  },
  watch: {
    registrationCompleted (val) {
      if (val) {
        const msg = 'Registration complete, check your email\n'
        const type = 'success'
        this.$emit('appAlert', { msg: msg, type: type })
        this.clearRegistrationStatus()
      }
    },
    registrationError (val) {
      if (val) {
        const msg = (
          'An error occurred while processing your request: ' + this.errMsg
        )
        const type = 'error'
        this.$emit('appAlert', { msg: msg, type: type })
        this.clearRegistrationStatus()
      }
    }
  },
  computed: Object.assign({},
    mapState('signup', [
      'registrationCompleted',
      'registrationError',
      'registrationLoading',
      'errMsg'
    ]),
    {
      usernameErrors () {
        const errors = []
        if (!this.$v.inputs.username.$dirty) return errors
        !this.$v.inputs.username.maxLength && errors.push(
          'Username must be at most 100 characters long')
        !this.$v.inputs.username.required && errors.push(
          'Username is required.')
        return errors
      },
      emailErrors () {
        const errors = []
        if (!this.$v.inputs.email.$dirty) return errors
        !this.$v.inputs.email.email && errors.push('Must be valid e-mail')
        !this.$v.inputs.email.required && errors.push('E-mail is required')
        return errors
      },
      pass1Errors () {
        const errors = []
        let confirmPass = this.inputs.password2
        let otherPass = this.inputs.password1
        if (!this.$v.inputs.password1.$dirty) return errors
        !this.$v.inputs.password1.minLength && errors.push(
          'At least 8 characters required')
        !this.$v.inputs.password1.required && errors.push(
          'Password is required.')
        !(confirmPass === otherPass) && errors.push(
          'Passwords do not match')
        return errors
      },
      pass2Errors () {
        const errors = []
        let confirmPass = this.inputs.password2
        let otherPass = this.inputs.password1
        if (!this.$v.inputs.password2.$dirty) return errors
        !this.$v.inputs.password2.minLength && errors.push(
          'At least 8 characters required')
        !this.$v.inputs.password2.required && errors.push(
          'Password is required.')
        !(confirmPass === otherPass) && errors.push(
          'Passwords do not match')
        return errors
      },
      alertStatus () {
        if (this.registrationCompleted || this.registrationError) {
          return true
        } else {
          return false
        }
      }
    }
  ),
  methods: Object.assign({},
    mapActions('signup', [
      'createAccount',
      'clearRegistrationStatus'
    ]),
    {
      submit: function () {
        // Validate inputs and login
        this.$v.$touch()
        if (!this.$v.$invalid) {
          let inputs = this.inputs
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
