import { expect } from 'chai';
import { shallowMount } from '@vue/test-utils';
import CountDown from '@/components/CountDown.vue';

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
      },
    })
    expect(wrapper.text()).to.include(timerText)
  })
})
