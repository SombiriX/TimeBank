<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" max-width="400">
        <v-form
          ref="taskInfo"
          v-model="taskInfoValid"
          @submit.prevent="submit()"
        >
          <v-card>
            <v-container grid-list-xs>
              <v-text-field
                autofocus
                label="Task Name"
                :rules=[rules.required]
                v-model="task_name"
              >
              </v-text-field>
              <v-text-field
                label="Task Notes"
                textarea
                v-model="task_notes"
              >
              </v-text-field>
            </v-container>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="accent"
                flat="flat"
                type="submit"
              >
                Update
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-dialog>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: 'taskInfo',
  props: {
    id: {
      type: Number,
      required: true
    },
    author: {
      type: String,
      required: true
    },
    intervals: {
      type: String,
      required: true
    },
    running_interval: {
      validator: (val) => {
        let ret = val instanceof Object
        return ret ? true : val === null
      },
      required: true
    },
    runtime: {
      type: Number,
      required: true
    },
    task_name: {
      type: String,
      required: true
    },
    task_notes: {
      type: String,
      required: true
    },
    task_type: {
      type: String,
      required: true
    },
    time_budget: {
      type: Number,
      required: true
    },
    complete: {
      type: Boolean,
      required: true
    },
    deleted: {
      type: Boolean,
      required: true
    },
    running: {
      type: Boolean,
      required: true
    },
    created: {
      type: String,
      required: true
    },
    last_added: {
      validator: (val) => {
        let ret = val instanceof String
        return ret ? true : val === null
      },
      required: true
    },
    last_modified: {
      type: String,
      required: true
    },
    parent_task: {
      validator: (val) => {
        let ret = val instanceof Number
        return ret ? true : val === null
      },
      required: true
    },
    tasklist: {
      type: Array,
      required: true
    }
  },
  data () {
    return {
      taskName: null,
      risk_fields: [],
      loading: false,
      dialog: true,
      taskInfoValid: false,
      rules: {
        required: value => !!value || 'Required.'
      }
    }
  },
  watch: {
    dialog (val) {
      this.$emit('taskInfoClose')
    }
  },
  mounted: function () {
    this.taskName = this.task_name
  },
  methods: {
    updateTask: function () {
      let taskData = {}
      this.$emit('updateTask', taskData)
    },
    emitNo: function () {
      this.$emit('taskInfoClose')
    },
    submit: function () {
      // Capture form submission
      if (this.$refs.taskInfo.validate()) {
        this.updateTask()
      }
    }
  }
}
</script>
