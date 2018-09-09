import api from '../api'
import {
  TASK_INIT_START,
  TASK_SUCCESS,
  TASK_FAIL,
  TASK_SET_TASK,
  TASK_SET_TASKLIST,
  TASK_DELETE_TASK,
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
  paused: false,
  interval: null
}

const getters = {
  taskRunning: state => !!state.running,
  runningTask: state => state.runningTaskId,
  completedTasks: (state) => {
    return state.tasks.filter(task => task.is_complete)
  },
  numCompleted: (state, getters) => {
    return getters.completedTasks.length
  }
}

const actions = {
  initialize ({ commit }) {
    // Get user's tasks
    commit(TASK_INIT_START)
    return api.getTasks()
      .then(({ data }) => commit(TASK_SET_TASKLIST, data))
      .then(() => commit(TASK_SUCCESS))
      .catch((err) => commit(TASK_FAIL, err))
  },
  createTask ({ commit }, task) {
    return api.addTask(task)
      .then(({ data }) => commit(TASK_SET_TASK, data))
      .then(() => commit(TASK_SUCCESS))
      .catch((err) => commit(TASK_FAIL, err))
  },
  deleteTask ({ commit }, taskId) {
    return api.deleteTask(taskId)
      .then(() => commit(TASK_DELETE_TASK, taskId))
      .then(() => commit(TASK_SUCCESS))
      .catch((err) => commit(TASK_FAIL, err))
  },
  runTask ({ commit, state }, taskId) {
    if (!state.running) {
      // Create interval
      const newInterval = {
        'task': taskId
      }
      return api.addInterval(newInterval)
        .then(({ data }) => commit(TASK_RUN, data))
        .then(() => commit(TASK_SUCCESS))
        .catch((err) => commit(TASK_FAIL, err))
    }
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
  [TASK_SET_TASK] (state, data) {
    state.tasks.push(data)
  },
  [TASK_SET_TASKLIST] (state, data) {
    state.tasks = data
  },
  [TASK_DELETE_TASK] (state, taskId) {
    state.tasks = state.tasks.filter(task => task.id !== taskId)
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
