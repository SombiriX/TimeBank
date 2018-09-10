<template>
  <v-container>
    <v-layout column align-center justify-center>
      <v-flex class="countdown">
        <span class="display-4">
          {{ timeLeft }}
        </span>
      </v-flex>
      <v-flex><span class="display-1">{{ endTime }}</span></v-flex>
    </v-layout>
  </v-container>
</template>

<script>
var intervalTimer

export default {
  props: {
    twentyFourClock: Boolean,
    time: Number,
    running: Boolean,
    paused: Boolean
  },
  data: function () {
    return {
      selectedTime: 0,
      timeLeft: '00:00',
      endTime: '0',
      secondsLeft: 0,
      dummy24Hr: this.twentyFourClock
    }
  },
  watch: {
    running: function (value) {
      // Start / stop the timer
      if (value) {
        // Start
        this.startCountDown(this.time)
      } else {
        // Stop
        this.startCountDown(0)
        this.endTime = '0'
      }
    },
    paused: function (value) {
      // Pause or resume the timer
      if (value) {
        // Pause
        clearInterval(intervalTimer)
      } else {
        // Resume
        this.startCountDown(this.secondsLeft)
      }
    }
  },
  methods: {
    startCountDown: function (seconds) {
      // Set the countdown time and clear any running timers
      clearInterval(intervalTimer)
      this._timer(seconds)
    },
    _timer: function (seconds) {
      // Determine end time and run the countdown to it
      const now = Date.now()
      const end = now + seconds * 1000
      this.displayTimeLeft(seconds)

      this.selectedTime = seconds
      this.displayEndTime(end)
      this._countdown(end)
    },
    _countdown: function (end) {
      intervalTimer = setInterval(() => {
        this.secondsLeft = Math.round((end - Date.now()) / 1000)

        if (this.secondsLeft === 0) {
          this.endTime = 0
        }

        if (this.secondsLeft < 0) {
          clearInterval(intervalTimer)
          return
        }
        this.displayTimeLeft(this.secondsLeft)
      }, 1000)
    },
    displayTimeLeft: function (secondsLeft) {
      const hours = Math.floor((secondsLeft % 216000) / 3600)
      const minutes = Math.floor((secondsLeft % 3600) / 60)
      const seconds = secondsLeft % 60

      const displayHours = secondsLeft >= 3600
      const displayMinutes = secondsLeft >= 60

      this.timeLeft = (
        `${displayHours ? zeroPadded(hours) + ':' : ''}` +
        `${displayMinutes ? zeroPadded(minutes) + ':' : ''}` +
        `${zeroPadded(seconds)}`
      )
    },
    displayEndTime: function (timestamp) {
      const end = new Date(timestamp)
      const hour = end.getHours()
      const minutes = end.getMinutes()

      let amPm = (hour < 12) ? 'AM' : 'PM'
      amPm = (this.dummy24Hr) ? '' : ' ' + amPm

      this.endTime = (
        `${hourConvert(hour, this.dummy24Hr)}:${zeroPadded(minutes)}` + amPm
      )
    }
  }
}

function zeroPadded (num) {
  // Pad numbers with 0 if less than 10
  return num < 10 ? `0${num}` : num
}

function hourConvert (hour, twentyFourClock) {
  // Display hour for 12 or 24 hour clock settings
  if (twentyFourClock) {
    return hour
  } else {
    return (hour % 12) || 12
  }
}
</script>
