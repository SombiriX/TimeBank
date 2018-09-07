import Vue from 'vue'
import Vuex from 'vuex'

// State Modules
import auth from './auth'
import password from './password'
import signup from './signup'
import task from './task'
import user from './user'

Vue.use(Vuex)

const debug = process.env.VUE_APP_DEBUG

export default new Vuex.Store({
  modules: {
    auth,
    password,
    signup,
    task,
    user
  },
  strict: debug
})
