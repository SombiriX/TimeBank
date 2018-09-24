import { expect } from 'chai'
import { shallowMount } from '@vue/test-utils'
import '../../src/plugins/vuetify'
import CountDown from '@/components/CountDown.vue'

describe('CountDown.vue', () => {
  it('Displays a 00:00 counter when not paused and not running', () => {
    const twentyFourClock = false
    const initialTime = 5
    const elapsedTime = 0
    const running = false
    const paused = false
    const timerText = '00:00'
    const wrapper = shallowMount(CountDown, {
      propsData: {
        twentyFourClock,
        initialTime,
        elapsedTime,
        running,
        paused
      }
    })
    expect(wrapper.text()).to.include(timerText)
  })

  it('Decrements the clock while running', (done) => {
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
    wrapper.vm.elapsedTime = 50
    wrapper.vm.running = true
    // console.log(wrapper.emitted('countDownTick'))
    // expect(wrapper.emitted('countDownTick')).to.be.true
    wrapper.vm.$nextTick(() => {
      expect(wrapper.vm.secondsLeft).to.be.above(0)
      done()
    })
  })
})
