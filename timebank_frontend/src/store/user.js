import api from '../api'
import {
  USER_INIT_START,
  USER_SUCCESS,
  USER_FAIL,
  USER_SET
} from './types'

const initialState = {
  loading: false,
  loaded: false,
  error: false,
  errorMsg: '',
  user: null
}

const getters = {
  hasInfo: state => state.loaded,
  userPrefs: state => state.user.user_prefs
}

const actions = {
  initialize ({ commit }) {
    // Get user's information
    commit(USER_INIT_START)
    return api.getUser()
      .then(({ data }) => commit(USER_SET, data))
      .then(() => commit(USER_SUCCESS))
      .catch((err) => commit(USER_FAIL, err))
  },
  updateUser ({ commit }, user) {
    return api.updateUser(user)
      .then(api.getUser())
      .then(({ data }) => commit(USER_SET, data))
      .then(() => commit(USER_SUCCESS))
      .catch((err) => commit(USER_FAIL, err))
  }
}

const mutations = {
  [USER_INIT_START] (state) {
    state.loading = true
    state.error = false
  },
  [USER_FAIL] (state, err) {
    state.loading = false
    state.error = true
    state.errorMsg = err
  },
  [USER_SUCCESS] (state) {
    state.loading = false
    state.error = false
    state.loaded = true
  },
  [USER_SET] (state, data) {
    state.user = data
  }
}

export default {
  namespaced: true,
  state: initialState,
  getters,
  actions,
  mutations
}
