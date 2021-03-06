<template>
  <v-container grid-list-md text-xs-center>
  <countdown
    :twentyFourClock = userPrefs.twentyFourClock
    :initialTime = initialTime
    :elapsedTime = elapsedTime
    :running = running
    :paused = paused
    @countDownTick="handleCountdownTick"
  ></countdown>
    <v-form
      ref="createTask"
      v-model="taskValid"
      @submit.prevent="create()"
    >
      <v-layout row>
        <v-flex xs10>
          <v-text-field
            v-model="newTask.task_name"
            label="What are you working on?"
            outline
            @keydown.enter="create"
            :rules="[rules.required]"
          >
          </v-text-field>
        </v-flex>
        <v-flex xs2>
          <v-text-field
            v-model="newTask.time_budget"
            name="name"
            label="Duration"
            outline
            placeholder="HH:MM"
            mask="time"
            return-masked-value
            append-icon="timer"
            @keydown.enter="create"
            :rules="[rules.required, rules.notZero]"
          ></v-text-field>
        </v-flex>
        <v-fade-transition slot="append">
          <v-btn
            flat
            icon
            v-if="newTask.task_name"
            @click="create"
          >
            <v-icon>add_circle</v-icon>
          </v-btn>
        </v-fade-transition>
      </v-layout>
    </v-form>
    <v-layout row wrap>
      <h2 class="display-1 text--primary pl-3">
        Tasks:&nbsp;
        <v-fade-transition leave-absolute>
          <span :key="`tasks-${tasks.length}`">
            {{ numCompleted + " / " + tasks.length }}
          </span>
        </v-fade-transition>
      </h2>
    </v-layout>
    <v-layout row wrap>
      <v-progress-linear
        :value="progress"
        color="white darken-3"
      ></v-progress-linear>
    </v-layout>

    <v-divider class="mt-3"></v-divider>

    <v-card v-if="tasks.length > 0">
      <v-slide-y-transition
        class="py-0"
        group
        tag="v-list"
      >
        <template
          v-for="(task, i) in tasks"
        >
          <v-divider
            v-if="i !== 0"
            :key="`${i}-divider`"
          ></v-divider>

          <!--TODO call setter-->
          <v-list-tile
            :key="`${i}-${task.task_name}`"
            @mouseover="task.active = true"
            @mouseleave="task.active = false"
            :color="task.running ? 'success' : ''"
          >
            <v-list-tile-action>
              <v-checkbox
                v-model="task.complete"
                color="info"
                @change="handleTaskComplete(task)"
              >
                <div
                  slot="label"
                  :class="task.complete && 'grey--text' || 'text--primary'"
                  class="ml-3"
                  v-text="task.task_name"
                ></div>
              </v-checkbox>
            </v-list-tile-action>

            <v-spacer></v-spacer>
            <v-divider class="mx-2" inset vertical></v-divider>
              {{ displayTaskTime(task) }}
            <v-divider class="mx-2" inset vertical></v-divider>
            <div  v-if="task.active">
              <v-btn v-if="!task.complete" flat icon @click="start(task)">
                <v-icon v-if="!task.running || paused">play_arrow</v-icon>
                <v-icon v-else>stop</v-icon>
              </v-btn>
              <v-btn v-if="task.running" flat icon @click="pause(task)">
                <v-icon>pause</v-icon>
              </v-btn>
              <v-btn
                flat
                icon
                @click="currentTask=tasks[i], dialogOrNull('taskInfo')"
              >
                <v-icon>info_outline</v-icon>
              </v-btn>
              <v-btn flat icon @click="remove(task.id)">
                <v-icon>remove_circle_outline</v-icon>
              </v-btn>
            </div>
          </v-list-tile>
        </template>
      </v-slide-y-transition>
    </v-card>
    <!-- User Action Dialogs -->
    <component
      :is="taskInfoDialog"
      v-bind="currentTask"
      @taskInfoClose="taskInfoClose()"
      @updateTask="handleUpdateTask"
    >
    </component>
  </v-container>
</template>

<script>
import countdown from '../components/CountDown'
import taskInfo from '../components/taskInfo'
import helpers from '../helpers'
import { mapGetters, mapState } from 'vuex'
import Vue from 'vue'

Vue.component('taskInfo', {
  template: taskInfo
})

export default {
  data: () => ({
    rules: {
      required: value => !!value || 'Required.',
      notZero: function (value) {
        const error = 'Time must be greater than zero'
        let zeroes = ['0', '00:', '00:0', '00:00']
        return !(zeroes.includes(value)) || error
      }
    },
    newTask: {
      task_name: '',
      time_budget: ''
    },
    taskValid: false,
    taskInfoDialog: null,
    currentTask: {}
  }),
  components: { countdown },
  computed: Object.assign({},
    mapState('task', [
      'loading',
      'error',
      'errorMsg',
      'running',
      'runningTaskId',
      'runningTaskIdx',
      'paused',
      'interval',
      'initialTime',
      'elapsedTime'
    ]),
    mapGetters('task', {
      taskRunning: 'taskRunning',
      completedTasks: 'completedTasks',
      numCompleted: 'numCompleted',
      getTaskById: 'getTaskById',
      tasks: 'tasks'
    }),
    mapGetters('user', {
      userPrefs: 'userPrefs'
    }),
    {
      progress: function () {
        return this.numCompleted / this.tasks.length * 100
      },
      remainingTasks: function () {
        return this.tasks.length - this.numCompleted
      }
    }
  ),
  mounted: function () {
    this.$store.dispatch('task/setTaskState')
  },
  methods: {
    create: function () {
      if (this.$refs.createTask.validate()) {
        // Call vuex action to create task
        let timeStr = this.padTime(this.newTask.time_budget)
        this.newTask.time_budget = helpers.toSeconds(timeStr)
        this.$store.dispatch('task/createTask', { ...this.newTask })

        // Reset fields and validation
        this.$refs.createTask.reset()
        this.newTask.task_name = ''
        this.newTask.time_budget = ''
      }
    },
    remove: function (id) {
      // Mark the task for deletion and alert user of the action
      this.$store.dispatch('task/deleteTask', id)
      const taskTxt = this.getTaskById(id).task_name
      const msg = 'Deleted: ' + taskTxt + ' UNDO?'
      const type = 'success'
      this.$emit('appAlert', { msg: msg, type: type })
    },
    start: function (task) {
      if (!task.running || this.paused) {
        // Call vuex runTask action
        this.$store.dispatch('task/runTask', task.id)
      } else {
        // Call vuex stopTask action
        this.$store.dispatch('task/stopTask', task.id)
      }
    },
    handleCountdownTick: function (status) {
      if (this.running) {
        // Update displayed time on the running task
        this.$store.dispatch('task/incrementTaskRuntime', 1)
      }
    },
    handleTaskComplete: function (task) {
      // Call vuex completeTask action
      this.$store.dispatch('task/completeTask', task.id)
    },
    handleUpdateTask: function (taskData) {
      // Call vuex updateTask action
      this.$store.dispatch('task/updateTask', taskData)
    },
    pause: function (task) {
      this.$store.dispatch('task/pauseTask', task.id)
    },
    padTime: function (timeStr) {
      // Takes a full or partial time string and
      // returns string formatted as HH:MM
      const components = this.$store.getters['task/getTimeObj'](timeStr)

      if (isNaN(components.minutes)) {
        return `${components.hours}:00`
      } else {
        return `${components.hours}:${components.minutes}`
      }
    },
    displayTaskTime: function (task) {
      const overtime = task.runtime > task.time_budget
      const absTime = Math.abs(task.time_budget - task.runtime)

      const timeObj = helpers.getTimeComponents(absTime)
      const newTime = helpers.getTimeStr(timeObj)

      const overage = overtime ? '+ ' : ''

      return overage + newTime
    },
    dialogOrNull: function (dialog) {
      if (dialog === 'taskInfo') {
        this.taskInfoDialog = taskInfo
      } else {
        this.taskInfoDialog = null
      }
    },
    taskInfoClose: function () {
      this.taskInfoDialog = null
    }
  }
}
</script>
