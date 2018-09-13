<template>
  <v-container grid-list-md text-xs-center>
  <countdown
    :twentyFourClock = countdown.twentyFourClock
    :time = time
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
              {{ task.time_budget }}
            <v-divider class="mx-2" inset vertical></v-divider>
            <div  v-if="task.active">
              <v-btn flat icon @click="start(task)">
                <v-icon v-if="!task.running || paused">play_arrow</v-icon>
                <v-icon v-else>stop</v-icon>
              </v-btn>
              <v-btn v-if="task.running" flat icon @click="pause(task)">
                <v-icon>pause</v-icon>
              </v-btn>
              <v-btn flat icon >
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
  </v-container>
</template>

<script>
import countdown from '../components/CountDown'
import helpers from '../helpers'
import { mapGetters, mapState } from 'vuex'

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
    countdown: {
      twentyFourClock: false // TODO replace with vuex state value
    }
  }),
  components: { countdown },
  computed: Object.assign({},
    mapState('task', [
      'loading',
      'error',
      'errorMsg',
      'tasks',
      'running',
      'runningTaskId',
      'runningTaskIdx',
      'paused',
      'interval',
      'time'
    ]),
    mapGetters('task', {
      taskRunning: 'taskRunning',
      completedTasks: 'completedTasks',
      numCompleted: 'numCompleted'
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
  methods: {
    create: function () {
      if (this.$refs.createTask.validate()) {
        // Call vuex action to create task
        this.newTask.time_budget = this.padTime(this.newTask.time_budget)
        this.$store.dispatch('task/createTask', { ...this.newTask })
        this.$refs.createTask.reset()
      }
    },
    remove: function (id) {
      this.$store.dispatch('task/deleteTask', id)
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
      // Update displayed time on the running task
      const timeObj = helpers.getTimeComponents(status.secondsLeft)
      const newTime = `${helpers.zeroPadded(timeObj.hours)}:` +
        `${helpers.zeroPadded(timeObj.minutes)}`
      const overage = status.overTime ? '+ ' : ''

      this.tasks[this.runningTaskIdx].time_budget = overage + newTime
    },
    handleTaskComplete: function (task) {
        // Call vuex completeTask action
        this.$store.dispatch('task/completeTask', task.id)
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
    }
  }
}

</script>
