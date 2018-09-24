<template>
  <v-container>
    <v-layout column align-center justify-center>
      <v-flex class="countdown">
        <span class="display-4">
          {{ overTime ? '+ ' + timeLeft : timeLeft }}
        </span>
      </v-flex>
      <v-flex><span class="display-1">{{ endTime }}</span></v-flex>
    </v-layout>
  </v-container>
</template>

<script>
// TODO handle pause unpause remaining time
export default {
  name: 'CountDown',
  props: {
    twentyFourClock: {
      type: Boolean,
      default: false
    },
    initialTime: {
      type: Number,
      required: true
    },
    elapsedTime: {
      type: Number
    },
    running: {
      type: Boolean,
      required: true
    },
    paused: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      timeLeft: '00:00',
      endTime: '0',
      secondsLeft: 0,
      overTime: false,
      dummy24Hr: this.twentyFourClock,
      intervalTimer: null
    }
  },
  watch: {
    running: function (value) {
      // Start / stop the timer
      if (value) {
        // Start
        if (this.initialTime >= this.elapsedTime) {
          // Count down
          this.overTime = false
          this.startCountDown(this.initialTime - this.elapsedTime)
        } else {
          // Count up
          this.overTime = true
          this.startCountDown(this.elapsedTime - this.initialTime)
        }
      } else {
        // Stop
        clearInterval(this.intervalTimer)
        this.endTime = '0'
        this.timeLeft = '00:00'
        this.overTime = false
      }
    },
    paused: function (value) {
      // Pause or resume the timer
      if (value) {
        // Pause
        clearInterval(this.intervalTimer)
      } else {
        // Resume
        if (!this.overTime) {
          this.startCountDown(this.secondsLeft)
        } else {
          this._countUp()
        }
      }
    }
  },
  methods: {
    startCountDown: function (seconds) {
      // Set the countdown time and clear any running timers
      clearInterval(this.intervalTimer)
      this._timer(seconds)
    },
    _timer: function (seconds) {
      // Determine end time and run the countdown to it
      const now = Date.now()
      const end = now + seconds * 1000
      this.displayTimeLeft(seconds)

      if (this.overTime) {
        this.secondsLeft = seconds
        this.displayEndTime(null)
        this._countUp()
      } else {
        this.displayEndTime(end)
        this._countDown(end)
      }
    },
    _countDown: function (end) {
      this.intervalTimer = setInterval(() => {
        this.secondsLeft = Math.round((end - Date.now()) / 1000)

        if (this.secondsLeft === 0) {
          // Countdown complete, display overage counter (count up)
          // this.endTime = 0
          // this.timeLeft = '00:00'
          this.$emit('countDownComplete')
          this.overTime = true
        }

        if (this.secondsLeft < 0) {
          clearInterval(this.intervalTimer)
          this.displayEndTime(null)
          this._countUp()
          return
        }
        this.displayTimeLeft(this.secondsLeft)
      }, 1000)
    },
    _countUp: function () {
      this.intervalTimer = setInterval(() => {
        this.secondsLeft = this.secondsLeft + 1
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
      let countdownStatus = {
        secondsLeft: this.secondsLeft,
        overTime: this.overTime
      }
      this.$emit('countDownTick', countdownStatus)
    },
    displayEndTime: function (timestamp) {
      if (timestamp === null) {
        this.endTime = ''
        return
      }

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
