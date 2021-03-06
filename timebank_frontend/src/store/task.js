import api from '../api'
import helpers from '../helpers'
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
  TASK_UPDATE
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
    return state.tasks.filter(task => (task.complete && !task.deleted))
  },
  deletedTasks: (state) => {
    return state.tasks.filter(task => task.deleted)
  },
  tasks: (state) => {
    return state.tasks.filter(task => !task.deleted)
  },
  recurringTasks: (state) => {
    return state.tasks.filter(task => task.task_type === 'C')
  },
  numCompleted: (state, getters) => {
    return getters.completedTasks.length
  },
  getTaskIdxById: (state) => (id) => {
    return state.tasks.findIndex(task => task.id === id)
  },
  getTaskById: (state) => (id) => {
    // Note: Returned value is read only
    return state.tasks.find(task => task.id === id)
  },
  getTimeObj: (state) => (timeStr) => {
    return helpers.convertTimeString(timeStr)
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
  _runTask ({ commit, getters, state }, taskId) {
    const newInterval = {
      'task': taskId
    }
    let taskIdx = getters.getTaskIdxById(taskId)
    return api.addInterval(newInterval)
      .then(({ data }) => commit(TASK_NEW_INTERVAL, data))
      .then(() => commit(TASK_RUN, taskIdx))
      .then(() => commit(TASK_SUCCESS))
      .catch((err) => commit(TASK_FAIL, err))
  },
  runTask ({ commit, dispatch, getters, state }, taskId) {
    if (!state.running || (state.paused && taskId === state.runningTaskId)) {
      // Create interval and start the timer
      return dispatch('_runTask', taskId)
    } else if (taskId !== state.runningTaskId) {
      // Stop existing timer and start timer for a different task
      return dispatch('stopTask', state.paused)
        .then(() => dispatch('_runTask', taskId))
    }
  },
  pauseTask ({ commit, state }, taskId) {
    if (state.running && !state.paused) {
      // Handle pausing
      commit(TASK_ADD_STOP_TIME, new Date().toISOString())
      return api.updateInterval({ ...state.interval })
        .then(commit(TASK_PAUSE))
        .catch((err) => commit(TASK_FAIL, err))
    }
  },
  stopTask ({ commit, state }) {
    // Stop running task and update interval if task is not
    // paused (interval already stopped)
    let action = state.paused ? v => Promise.resolve(v) : api.updateInterval
    state.paused = false
    commit(TASK_ADD_STOP_TIME, new Date().toISOString())
    return action({ ...state.interval })
      .then(commit(TASK_STOP))
      .catch((err) => commit(TASK_FAIL, err))
  },
  completeTask ({ dispatch, commit, getters, state }, taskId) {
    // Update the task's complete flag
    if (state.running && (state.runningTaskId === taskId)) {
      // Stop the timer if task to complete is running
      dispatch('stopTask', taskId)
    }

    let taskIdx = getters.getTaskIdxById(taskId)
    return api.updateTask({ ...state.tasks[taskIdx] })
      .catch((err) => commit(TASK_FAIL, err))
  },
  updateTask ({ commit, getters }, taskData) {
    let taskIdx = { idx: getters.getTaskIdxById(taskData.id) }
    return api.updateTask({ ...taskData })
      .then(commit(TASK_UPDATE, { ...taskIdx, ...taskData }))
      .catch((err) => commit(TASK_FAIL, err))
  },
  incrementTaskRuntime ({ commit, state }, increment) {
    state.tasks[state.runningTaskIdx].runtime += increment
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
  [TASK_SET_STATE] (state) {
    const running = state.tasks.filter(task => task.running)
    if (running.length === 1) {
      const runningTask = running[0]
      let taskIdx = state.tasks.findIndex(task => task.id === runningTask.id)

      state.initialTime = runningTask.time_budget
      state.elapsedTime = runningTask.runtime
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
    state.elapsedTime = state.tasks[taskIdx].runtime
    state.initialTime = state.tasks[taskIdx].time_budget
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
  [TASK_STOP] (state) {
    state.running = false
    state.runningTaskId = null
    state.interval = null
    state.tasks[state.runningTaskIdx].running = false
    state.runningTaskIdx = null
  },
  [TASK_PAUSE] (state) {
    state.paused = true
  },
  [TASK_UPDATE] (state, data) {
    state.tasks[data.idx].task_name = data.task_name
    state.tasks[data.idx].task_notes = data.task_notes
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
