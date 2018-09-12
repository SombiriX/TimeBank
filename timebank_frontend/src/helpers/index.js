export default {
  getTimeComponents: function (secondsLeft) {
    const hours = Math.floor((secondsLeft % 216000) / 3600)
    const minutes = Math.floor((secondsLeft % 3600) / 60)
    const seconds = secondsLeft % 60

    return {
      hours: hours,
      minutes: minutes,
      seconds: seconds
    }
  },
  zeroPadded: function (num) {
    // Pad numbers with 0 if less than 10
    return num < 10 ? `0${num}` : num
  }
}
