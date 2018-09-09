<template>
  <v-container grid-list-md text-xs-center>
  <countdown
    v-bind:twentyFourClock = countdown.twentyFourClock
    v-bind:time = countdown.time
    v-bind:running = countdown.running
    v-bind:paused = countdown.paused
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

          <v-list-tile
            :key="`${i}-${task.task_name}`"
            @mouseover="task.active = true"
            @mouseleave="task.active = false"
          >
            <v-list-tile-action>
              <v-checkbox
                v-model="task.is_complete"
                color="info"
              >
                <div
                  slot="label"
                  :class="task.is_complete && 'grey--text' || 'text--primary'"
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
                <v-icon>play_arrow</v-icon>
              </v-btn>
              <v-btn flat icon @click="pause(task)">
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
import { mapGetters, mapState } from 'vuex'

export default {
  data: () => ({
    rules: {
      required: value => !!value || 'Required.',
      notZero: function (value) {
        const entry = convertTimeString(value)
        const hasHours = entry.hours > 0
        const hasMinutes = entry.minutes > 0
        const error = 'Time must be greater than zero'
        return (hasHours || hasMinutes) || error
      }
    },
    newTask: {
      task_name: '',
      time_budget: ''
    },
    taskValid: false,
    countdown: {
      twentyFourClock: false,
      time: 0,
      running: false,
      paused: false
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
      'paused',
      'interval'
    ]),
    mapGetters('task', {
      taskRunning: 'taskRunning',
      runningTask: 'runningTask',
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
        const newTask = {
          task_name: this.newTask.task_name,
          time_budget: this.newTask.time_budget
        }
        this.$store.dispatch('task/createTask', newTask)
        this.$refs.createTask.reset()
      }
    },
    remove: function (id) {
      this.$store.dispatch('task/deleteTask', id)
    },
    start: function (task) {
      // Call vuex runTask action
      this.$store.dispatch('task/runTask', task.id)
    },
    pause: function (task) {
      this.countdown.paused = true
    }
  }
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
  // Convert time string to seconds
  const time = convertTimeString(timeStr)
  let seconds = 0

  seconds += 60 * 60 * time.hours
  seconds += 60 * time.minutes

  return seconds
}
</script>
