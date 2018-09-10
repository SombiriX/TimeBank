import api from '../api'
import {
  TASK_INIT_START,
  TASK_SUCCESS,
  TASK_FAIL,
  TASK_SET_TASK,
  TASK_SET_TASKLIST,
  TASK_DELETE_TASK,
  TASK_RUN,
  TASK_NEW_INTERVAL,
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
  interval: null,
  time: 0
}

const getters = {
  taskRunning: state => !!state.running,
  runningTask: state => state.runningTaskId,
  completedTasks: (state) => {
    return state.tasks.filter(task => task.is_complete)
  },
  numCompleted: (state, getters) => {
    return getters.completedTasks.length
  },
  getTaskIdxById: (state) => (id) => {
    return state.tasks.findIndex(task => task.id === id)
  },
  getTimeObj: (state) => (timeStr) => {
    return convertTimeString(timeStr)
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
    // TODO Handle case where timer is running
    return api.deleteTask(taskId)
      .then(() => commit(TASK_DELETE_TASK, taskId))
      .then(() => commit(TASK_SUCCESS))
      .catch((err) => commit(TASK_FAIL, err))
  },
  runTask ({ commit, state, getters }, taskId) {
    if (!state.running) {
      // Create interval and start the timer
      const newInterval = {
        'task': taskId
      }
      let taskIdx = getters.getTaskIdxById(taskId)
      return api.addInterval(newInterval)
        .then(({ data }) => commit(TASK_NEW_INTERVAL, data))
        .then(() => commit(TASK_RUN, taskIdx))
        .then(() => commit(TASK_SUCCESS))
        .catch((err) => commit(TASK_FAIL, err))
    } else if (taskId !== state.runningTaskId) {
      // TODO Pause existing timer and start timer for a different task
    }
  },
  pauseTask ({ commit, state, getters }, taskId) {
    if (state.running) {
      // TODO handle pausing
    }
  },
  stopTask ({ commit, state, getters }, taskId) {
    // Update interval
    let taskIdx = getters.getTaskIdxById(taskId)
    commit(TASK_ADD_STOP_TIME, new Date().toISOString())
    return api.updateInterval({ ...state.interval })
      .then(commit(TASK_STOP, taskIdx))
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
    state.tasks.push(addFrontendFields(data))
  },
  [TASK_SET_TASKLIST] (state, data) {
    state.tasks = addFrontendFields(data)
  },
  [TASK_DELETE_TASK] (state, taskId) {
    state.tasks = state.tasks.filter(task => task.id !== taskId)
  },
  [TASK_RUN] (state, taskIdx) {
    state.time = toSeconds(state.tasks[taskIdx].time_budget)
    state.running = true
    state.tasks[taskIdx].running = true
  },
  [TASK_NEW_INTERVAL] (state, interval) {
    state.runningTaskId = interval.task
    state.interval = interval
  },
  [TASK_ADD_STOP_TIME] (state, stopTime) {
    state.interval.stop = stopTime
  },
  [TASK_STOP] (state, taskIdx) {
    state.running = false
    state.runningTaskId = null
    state.interval = null
    state.tasks[taskIdx].running = false
  }
}

export default {
  namespaced: true,
  state: initialState,
  getters,
  actions,
  mutations
}

function addFrontendFields (tasks) {
  // Add fields to task objects which are only used on the frontend
  if (Array.isArray(tasks)) {
    // Add fields for task list
    return tasks.map((task) => {
      return _addFields(task)
    })
  } else {
    // Add fields for single task
    return _addFields(tasks)
  }
}

function _addFields (task) {
  let addFields = {
    active: false,
    running: false
  }
  return { ...task, ...addFields }
}

function convertTimeString (timeStr) {
  // Split string into hours and minutes
  const components = timeStr.split(':')
  const hours = parseInt(components[0], 10)
  const minutes = parseInt(components[1], 10)

  return {
    'hours': hours,
    'minutes': minutes
  }
}

function toSeconds (timeStr) {
  // Convert HH:SS time string to seconds
  const time = convertTimeString(timeStr)
  let seconds = 0

  seconds += 60 * 60 * time.hours
  seconds += 60 * time.minutes

  return seconds
}
