<template>
  <v-container>
  <countdown v-bind:twentyFourClock=false></countdown>
    <v-form
      ref="createTask"
      v-model="taskValid"
      @submit.prevent="create()"
    >
      <v-layout row>
        <v-flex xs10>
          <v-text-field
            v-model="newTask.name"
            label="What are you working on?"
            outline
            @keydown.enter="create"
            :rules="[rules.required]"
          >
          </v-text-field>
        </v-flex>
        <v-flex xs2>
          <v-text-field
            name="name"
            label="Duration"
            outline
            placeholder="HH:MM"
            mask="##:##"
            append-icon="timer"
            @keydown.enter="create"
            :rules="[rules.required]"
          ></v-text-field>
        </v-flex>
        <v-fade-transition slot="append">
          <v-btn
            flat
            icon
            v-if="newTask.name"
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
            {{ completedTasks + " / " + tasks.length }}
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
        <template v-for="(task, i) in tasks">
          <v-divider
            v-if="i !== 0"
            :key="`${i}-divider`"
          ></v-divider>

          <v-list-tile :key="`${i}-${task.text}`">
            <v-list-tile-action>
              <v-checkbox
                v-model="task.done"
                color="info"
              >
                <div
                  slot="label"
                  :class="task.done && 'grey--text' || 'text--primary'"
                  class="ml-3"
                  v-text="task.text"
                ></div>
              </v-checkbox>
            </v-list-tile-action>

            <v-spacer></v-spacer>
            <v-divider inset vertical></v-divider>
            {{ task.duration }}
            <v-divider inset vertical></v-divider>
            <v-btn flat icon >
              <v-icon>play_arrow</v-icon>
            </v-btn>
            <v-btn flat icon >
              <v-icon>pause</v-icon>
            </v-btn>
            <v-divider inset vertical></v-divider>
            <v-btn flat icon >
              <v-icon>info_outline</v-icon>
            </v-btn>
            <v-divider inset vertical></v-divider>
            <v-btn flat icon @click="remove(task.id)">
              <v-icon>remove_circle_outline</v-icon>
            </v-btn>
          </v-list-tile>
        </template>
      </v-slide-y-transition>
    </v-card>
  </v-container>
</template>

<script>
import countdown from '../components/CountDown'

export default {
  data: () => ({
    tasks: [
      {
        id: 1,
        done: false,
        text: 'Foobar',
        duration: "1:33"
      },
      {
        id: 2,
        done: false,
        text: 'Fizzbuzz',
        duration: "1:33"
      }
    ],
    rules: {
      required: value => !!value || 'Required.'

    },
    newTask: {
      name: null,
      duration: 0
    }
  }),
  components: { countdown },
  computed: {
    completedTasks: function () {
      return this.tasks.filter(task => task.done).length
    },
    progress: function () {
      return this.completedTasks / this.tasks.length * 100
    },
    remainingTasks: function () {
      return this.tasks.length - this.completedTasks
    }
  },

  methods: {
    create: function () {
      if (this.$refs.createTask.validate()) {
        this.tasks.push({
          done: false,
          text: this.newTask.name
        })
        this.$refs.createTask.reset()
      }
    },
    remove: function (id) {
      this.tasks = this.tasks.filter(function (task) {
        if (task.id != id) {
          return task
        }
      })
    }
  }
}
</script>
