import { expect } from 'chai'
import lolex from 'lolex'
import { shallowMount } from '@vue/test-utils'
import '../../src/plugins/vuetify'
import CountDown from '@/components/CountDown.vue'

describe('CountDown.vue', function () {
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
    this.clock = lolex.install()
  })

  afterEach(function () {
    this.clock.uninstall()
  })

  it('Displays a 00:00 counter when not paused and not running', function () {
    const data = {
      twentyFourClock: false,
      initialTime: 0,
      elapsedTime: 0,
      running: false,
      paused: false
    }

    const wrapper = shallowMount(CountDown, {
      propsData: data
    })
    expect(wrapper.text()).to.include(timerText.default)
  })

  it('Sets initial time while running', function (done) {
    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 0,
      running: false,
      paused: false
    }

    const wrapper = shallowMount(CountDown, {
      propsData: data
    })

    // Check initial time
    wrapper.setProps({
      running: true
    })

    wrapper.vm.$nextTick(() => {
      expect(wrapper.text()).to.include(timerText.initial)
      done()
    })
  })

  it('Decrements the clock while running', function (done) {
    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 0,
      running: false,
      paused: false
    }

    const wrapper = shallowMount(CountDown, {
      propsData: data
    })

    // Check with elapsed time
    wrapper.setProps({
      elapsedTime: 20,
      running: true
    })

    wrapper.vm.$nextTick(() => {
      expect(wrapper.text()).to.include(timerText.elapsed)
      done()
    })
  })

  it('Changes display format when past the initial time', function (done) {
    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 0,
      running: false,
      paused: false
    }

    const wrapper = shallowMount(CountDown, {
      propsData: data
    })

    // Check with overage time
    wrapper.setProps({
      elapsedTime: 3720,
      running: true
    })

    wrapper.vm.$nextTick(() => {
      expect(wrapper.text()).to.include(timerText.overtime)
      done()
    })
  })

  it('Displays time in 24 hr format when preferred', function (done) {
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
      running: false,
      paused: false
    }

    const wrapper = shallowMount(CountDown, {
      propsData: data
    })

    wrapper.setProps({
      running: true
    })

    wrapper.vm.$nextTick(() => {
      expect(wrapper.text()).to.include(timerText.twentyFourTime)
      done()
    })
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
      running: false,
      paused: false
    }

    const wrapper = shallowMount(CountDown, {
      propsData: data
    })

    wrapper.setProps({
      running: true
    })

    wrapper.vm.$nextTick(() => {
      expect(wrapper.text()).to.include(timerText.regTime)
      done()
    })
  })

  it('Can be paused and unpaused', function () {
    this.timeout(5000)
    const data = {
      twentyFourClock: false,
      initialTime: 60,
      elapsedTime: 0,
      running: false,
      paused: false
    }

    const wrapper = shallowMount(CountDown, {
      propsData: data
    })

    // Check with overage time
    wrapper.setProps({
      running: true
    })
    this.clock.tick(500)
    expect(wrapper.text()).to.include(timerText.initial)
    this.clock.tick(1000)
    expect(wrapper.text()).to.include(timerText.unpaused1)

    wrapper.setProps({
      paused: true
    })

    this.clock.tick(5000)
    expect(wrapper.text()).to.include(timerText.unpaused1)

    wrapper.setProps({
      paused: false
    })

    this.clock.tick(10000)
    expect(wrapper.text()).to.include(timerText.unpaused2)
  })
})
