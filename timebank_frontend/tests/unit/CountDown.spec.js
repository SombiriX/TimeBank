import lolex from 'lolex'
import { mount } from '@vue/test-utils'
import Vue from 'vue'
import Vuetify from 'vuetify'
import CountDown from '@/components/CountDown.vue'

Vue.use(Vuetify)

describe('CountDown.vue', function () {
  let wrapper
  let clock
  const timerText = {
    default: '00:00',
    initial: '01:00',
    elapsed: '40',
    unpaused1: '59',
    unpaused2: '49',
    overtime: '+ 01:01:00',
    twentyFourTime: '15:00',
    regTime: '3:00 PM'
  }

  // Mock setTimeout function
  beforeEach(function () {
    const defaultData = {
      twentyFourClock: false,
      initialTime: 0,
      elapsedTime: 0,
      running: false,
      paused: false
    }

    wrapper = mount(CountDown, {
      propData: defaultData
    })

    clock = lolex.install()
  })

  afterEach(function () {
    clock.uninstall()
  })

  it('Displays a 00:00 counter when not paused and not running', function () {
    const data = {
      twentyFourClock: false,
      initialTime: 0,
      elapsedTime: 0,
      running: false,
      paused: false
    }

    wrapper.setProps(data)

    expect(wrapper.text()).toContain(timerText.default)
  })

  it('Sets initial time while running', function (done) {
    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 0,
      running: true,
      paused: false
    }

    wrapper.setProps(data)

    wrapper.vm.$nextTick(() => {
      expect(wrapper.text()).toContain(timerText.initial)
      done()
    })
  })

  it('Decrements the clock while running', function (done) {
    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 20,
      running: true,
      paused: false
    }

    wrapper.setProps(data)

    wrapper.vm.$nextTick(() => {
      expect(wrapper.text()).toContain(timerText.elapsed)
      done()
    })
  })

  it('Changes display format when past the initial time', function (done) {
    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 3720,
      running: true,
      paused: false
    }

    wrapper.setProps(data)

    wrapper.vm.$nextTick(() => {
      expect(wrapper.text()).toContain(timerText.overtime)
      done()
    })
  })

  it('Displays time in 24 hr format when preferred', function () {
    const constantDate = new Date('2017-06-13T15:00:00')

    /* eslint no-global-assign:off */
    Date = class extends Date {
      constructor () {
        return constantDate
      }
    }

    const data = {
      twentyFourClock: true,
      initialTime: 60,
      elapsedTime: 0,
      running: true,
      paused: false
    }

    wrapper.setProps(data)
    
    expect(wrapper.text()).toContain(timerText.twentyFourTime)
  })

  it('Displays time in regular format when preferred', function (done) {
    const constantDate = new Date('2017-06-13T15:00:00')

    /* eslint no-global-assign:off */
    Date = class extends Date {
      constructor () {
        return constantDate
      }
    }

    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 0,
      running: true,
      paused: false
    }

    wrapper.setProps(data)

    wrapper.vm.$nextTick(() => {
      expect(wrapper.text()).toContain(timerText.regTime)
      done()
    })
  })

  it('Can be paused and unpaused', function () {
    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 0,
      running: true,
      paused: false
    }

    wrapper.setProps(data)

    clock.tick(500)
    expect(wrapper.text()).toContain(timerText.initial)
    clock.tick(1000)
    expect(wrapper.text()).toContain(timerText.unpaused1)

    wrapper.setProps({
      paused: true
    })

    clock.tick(5000)
    expect(wrapper.text()).toContain(timerText.unpaused1)

    wrapper.setProps({
      paused: false
    })

    clock.tick(10000)
    expect(wrapper.text()).toContain(timerText.unpaused2)
  })

  it('Emits an event for each tick', function () {
    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 0,
      running: true,
      paused: false
    }

    wrapper.setProps(data)

    clock.tick(5000)
    const emissions = wrapper.emitted().countDownTick

    // Countdown setup code calls displaytime which triggers event,
    // The event then fires once/ second afterwards
    expect(emissions.length).toBe(1 + 5)
    expect(emissions[0][0]).toMatchObject({'secondsLeft': 0, 'overTime': false})
    expect(emissions[1][0]).toMatchObject({'secondsLeft': 59, 'overTime': false})
    expect(emissions[2][0]).toMatchObject({'secondsLeft': 58, 'overTime': false})
    expect(emissions[3][0]).toMatchObject({'secondsLeft': 57, 'overTime': false})
    expect(emissions[4][0]).toMatchObject({'secondsLeft': 56, 'overTime': false})
    expect(emissions[5][0]).toMatchObject({'secondsLeft': 55, 'overTime': false})
  })

  it('Emits an event when complete', function () {
    const data = {
      twentyFourClock: false,
      initialTime: 5,
      elapsedTime: 0,
      running: true,
      paused: false
    }

    wrapper.setProps(data)

    clock.tick(6000)
    const emissions = wrapper.emitted().countDownComplete

    expect(emissions.length).toBe(1)
  })
})
