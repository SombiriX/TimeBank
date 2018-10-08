<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-container grid-list-xs>
            <v-card-title class="headline">
              {{ task_name }}
            </v-card-title>
          </v-container>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="success"
              flat="flat"
              @click.native="dialog = false, emitNo()"
            >
                NO
            </v-btn>
            <v-btn
              color="error"
              flat="flat"
              @click.native="dialog = false, emitYes()"
            >
                YES
            </v-btn>
          </v-card-actions>
        </v-card>
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
      risk_fields: [],
      loading: false,
      dialog: true,
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
  },
  methods: {
    emitYes: function () {
      this.$emit('dialogYes')
    },
    emitNo: function () {
      this.$emit('taskInfoClose')
    }
  }
}
</script>
