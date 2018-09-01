import Vue from 'vue'
import Vuex from 'vuex'

// State Modules
import auth from './auth'
import password from './password'
import signup from './signup'

Vue.use(Vuex)

const debug = process.env.VUE_APP_DEBUG

export default new Vuex.Store({
  modules: {
    auth,
    password,
    signup
  },
  strict: debug
})
