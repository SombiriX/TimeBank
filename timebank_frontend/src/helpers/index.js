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
  },
  convertTimeString: function (timeStr) {
    // Split string into hours and minutes
    const components = timeStr.split(':')
    const hours = parseInt(components[0], 10)
    const minutes = parseInt(components[1], 10)

    return {
      'hours': hours,
      'minutes': minutes
    }
  },
  getTimeStr: function (timeObj) {
    const newTime = `${this.zeroPadded(timeObj.hours)}:` +
      `${this.zeroPadded(timeObj.minutes)}`
    return newTime
  },
  toSeconds: function (timeStr) {
    // Convert HH:SS time string to seconds
    const time = this.convertTimeString(timeStr)
    let seconds = 0

    seconds += 60 * 60 * time.hours
    seconds += 60 * time.minutes

    return seconds
  }
}
