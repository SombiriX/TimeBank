import api from '../api'
import {
  TASK_INIT_START,
  TASK_SUCCESS,
  TASK_FAIL,
  TASK_SET_TASK,
  TASK_SET_TASKLIST,
  TASK_SET_STATE,
  TASK_DELETE_TASK,
  TASK_RUN,
  TASK_NEW_INTERVAL,
  TASK_ADD_STOP_TIME,
  TASK_STOP,
  TASK_PAUSE,
  TASK_COMPLETE
} from './types'

const initialState = {
  loading: false,
  error: false,
  errorMsg: '',
  tasks: [],
  running: false,
  runningTaskId: null,
  runningTaskIdx: null,
  paused: false,
  interval: null,
  initialTime: 0,
  elapsedTime: 0
}

const getters = {
  taskRunning: state => !!state.running,
  completedTasks: (state) => {
    return state.tasks.filter(task => task.complete)
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
  setTaskState ({ commit }) {
    return commit(TASK_SET_STATE)
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
    if (!state.running || (state.paused && taskId === state.runningTaskId)) {
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
      // TODO Stop existing timer and start timer for a different task
    }
  },
  pauseTask ({ commit, state, getters }, taskId) {
    if (state.running && !state.paused) {
      // Handle pausing
      commit(TASK_ADD_STOP_TIME, new Date().toISOString())
      return api.updateInterval({ ...state.interval })
        .then(commit(TASK_PAUSE))
        .catch((err) => commit(TASK_FAIL, err))
    }
  },
  stopTask ({ commit, state, getters }, taskId) {
    // Update interval
    commit(TASK_ADD_STOP_TIME, new Date().toISOString())
    return api.updateInterval({ ...state.interval })
      .then(commit(TASK_STOP))
      .catch((err) => commit(TASK_FAIL, err))
  },
  completeTask ({ actions, commit, getters, state }, taskId) {
    // Update task's complete flag
    if (state.running) {
      actions.stopTask(taskId)
    }
    let taskIdx = getters.getTaskIdxById(taskId)
    commit(TASK_COMPLETE, taskIdx)
    return api.updateTask({ ...state.tasks[taskIdx] })
      .catch((err) => commit(TASK_FAIL, err))
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
    // TODO check to see if task is running, if running, get and store the interval and set up state and timer
  },
  [TASK_SET_TASKLIST] (state, data) {
    state.tasks = addFrontendFields(data)
  },
  [TASK_SET_STATE] (state) {
    const running = state.tasks.filter(task => task.running)
    if (running.length === 1) {
      const runningTask = running[0]
      let taskIdx = state.tasks.findIndex(task => task.id === runningTask.id)

      state.initialTime = toSeconds(runningTask.time_budget)
      state.elapsedTime = Math.round(runningTask.runtime)
      state.running = true
      state.paused = false
      state.runningTaskIdx = taskIdx
      state.runningTaskId = runningTask.id
      state.interval = runningTask.running_interval
    } else if (running.length > 1) {
      throw Error('Multiple running tasks is an invalid state')
    }
  },
  [TASK_DELETE_TASK] (state, taskId) {
    state.tasks = state.tasks.filter(task => task.id !== taskId)
  },
  [TASK_RUN] (state, taskIdx) {
    state.elapsedTime = 0
    state.initialTime = toSeconds(state.tasks[taskIdx].time_budget)
    state.running = true
    state.paused = false
    state.tasks[taskIdx].running = true
    state.runningTaskIdx = taskIdx
  },
  [TASK_NEW_INTERVAL] (state, interval) {
    state.runningTaskId = interval.task
    state.interval = interval
  },
  [TASK_ADD_STOP_TIME] (state, stopTime) {
    state.interval.stop = stopTime
  },
  [TASK_COMPLETE] (state, taskIdx) {
    state.tasks[taskIdx].complete = true
  },
  [TASK_STOP] (state) {
    state.running = false
    state.runningTaskId = null
    state.interval = null
    state.tasks[state.runningTaskIdx].running = false
    state.runningTaskIdx = null
  },
  [TASK_PAUSE] (state) {
    state.paused = true
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
    active: false
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
