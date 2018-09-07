import api from '../api'
import {
  TASK_INIT_START,
  TASK_SUCCESS,
  TASK_FAIL,
  TASK_SET,
  TASK_RUN,
  TASK_ADD_STOP_TIME,
  TASK_STOP
} from './types'

const initialState = {
  loading: false,
  error: false,
  errorMsg: '',
  tasks: [],
  running: false,
  runningTaskId: null,
  interval: null
}

const getters = {
  taskRunning: state => !!state.running,
  runningTask: state => state.runningTaskId
}

const actions = {
  initialize ({ commit }) {
    // Get user's tasks
    commit(TASK_INIT_START)
    return api.getTasks()
      .then(({ data }) => commit(TASK_SET, data))
      .then(() => commit(TASK_SUCCESS))
      .catch((err) => commit(TASK_FAIL, err))
  },
  createTask ({ commit }, task) {
    return api.addTask(task)
      .then(api.getTasks())
      .then(({ data }) => commit(TASK_SET, data))
      .then(() => commit(TASK_SUCCESS))
      .catch((err) => commit(TASK_FAIL, err))
  },
  deleteTask ({ commit }, taskId) {
    return api.deleteTask(taskId)
      .then(api.getTasks())
      .then(({ data }) => commit(TASK_SET, data))
      .then(() => commit(TASK_SUCCESS))
      .catch((err) => commit(TASK_FAIL, err))
  },
  runTask ({ commit }, taskId) {
    // Create interval
    const newInterval = {
      'start': Date.now(),
      'task': taskId
    }
    return api.addInterval(newInterval)
      .then(({ data }) => commit(TASK_RUN, data))
      .then(() => commit(TASK_SUCCESS))
      .catch((err) => commit(TASK_FAIL, err))
  },
  stopTask ({ commit, state }, taskId) {
    // Update interval
    commit(TASK_ADD_STOP_TIME, Date.now())
    return api.updateInterval(state.interval, state.interval.id)
      .then(commit(TASK_STOP, state.interval))
  }
}

const mutations = {
  [TASK_INIT_START] (state) {
    state.loading = true
    state.error = false
  },
  [TASK_FAIL] (state, err) {
    state.loading = false
    state.error = true
    state.errorMsg = err
  },
  [TASK_SUCCESS] (state) {
    state.loading = false
    state.error = false
  },
  [TASK_SET] (state, data) {
    state.tasks = data
  },
  [TASK_RUN] (state, interval) {
    state.running = true
    state.runningTaskId = interval.task
    state.interval = interval
  },
  [TASK_ADD_STOP_TIME] (state, stopTime) {
    state.interval.stop = stopTime
  },
  [TASK_STOP] (state) {
    state.running = false
    state.runningTaskId = null
    state.interval = null
  }
}

export default {
  namespaced: true,
  state: initialState,
  getters,
  actions,
  mutations
}
