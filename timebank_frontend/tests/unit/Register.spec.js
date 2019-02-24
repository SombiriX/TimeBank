import { mount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import Vuetify from 'vuetify'
import Register from '@/views/Register.vue'

describe('Register.vue', () => {
  const localVue = createLocalVue()
  localVue.use(Vuex)
  localVue.use(VueRouter)
  localVue.use(Vuetify)

  // Mock up some testing functions and data
  let wrapper
  let actions
  let modules
  let signup
  let state
  let store
  let fakeCreateAccount
  let expectSuccess

  const validData = {
    username: 'TEST_PASS',
    password1: 'qweasdzx',
    password2: 'qweasdzx',
    email: 'test@example.com'
  }
  const badServerResponse = {
    username: 'TEST_FAIL',
    password1: 'qweasdzx',
    password2: 'qweasdzx',
    email: 'test@example.com'
  }
  const invalidData1 = {
    username: 'TEST_FAIL',
    password1: 'qweasdz',
    password2: 'qweasdz',
    email: 'test@example.com'
  }
  const invalidData2 = {
    username: 'TEST_FAIL',
    password1: 'qweasdzxABC',
    password2: 'qweasdzx',
    email: 'test@example.com'
  }
  const invalidData3 = {
    username: 'TEST_FAIL',
    password1: 'qweasdzx',
    password2: 'qweasdzxABC',
    email: 'test@example.com'
  }
  const invalidData4 = {
    username: 'TEST_FAIL',
    password1: 'qweasdzx',
    password2: 'qweasdzx',
    email: 'test@example'
  }

  const routes = [
    { path: '/login', name: 'login' }
  ]
  const router = new VueRouter({ routes })

  beforeEach(() => {
    state = {
      registrationCompleted: false,
      registrationError: false,
      registrationLoading: false,
      errMsg: ''
    }

    fakeCreateAccount = function () {
      if (expectSuccess) {
        state.registrationCompleted = true
      } else {
        state.errMsg = 'BIG FAIL'
        state.registrationError = true
      }
    }

    actions = {
      createAccount: fakeCreateAccount,
      clearRegistrationStatus: jest.fn()
    }

    signup = {
      namespaced: true,
      state,
      actions
    }

    modules = { signup }

    store = new Vuex.Store({ modules })

    wrapper = mount(Register, {
      localVue: localVue,
      store,
      router
    })
  })

  test('Calls createAccount, emits success, and clears on valid reg', () => {
    // Set valid data
    wrapper.setData({
      inputs: {
        username: validData.username,
        password1: validData.password1,
        password2: validData.password2,
        email: validData.email
      }
    })

    // Cause submission
    let btn = wrapper.find({ ref: 'registerForm' })
    expect(btn).toBeDefined()
    expectSuccess = true
    btn.trigger('submit.prevent')

    // Expect component to trigger state actions
    expect(wrapper.vm.registrationCompleted).toBe(true)
    expect(wrapper.vm.registrationError).toBe(false)
    expect(wrapper.vm.registrationLoading).toBe(false)
    expect(wrapper.vm.errMsg).toBe('')

    // Expect success emission
    const emissions = wrapper.emitted().appAlert
    expect(emissions.length).toBe(1)
    const msg = 'Registration complete, check your email\n'
    expect(emissions[0][0]).toMatchObject({ 'msg': msg, 'type': 'success' })

    // Expect cleanup action
    expect(actions.clearRegistrationStatus).toHaveBeenCalled()
  })

  test('Calls createAccount, emits failure, and clears on invalid reg', () => {
    // Set valid data
    wrapper.setData({
      inputs: {
        username: badServerResponse.username,
        password1: badServerResponse.password1,
        password2: badServerResponse.password2,
        email: badServerResponse.email
      }
    })

    // Cause submission
    let btn = wrapper.find({ ref: 'registerForm' })
    expect(btn).toBeDefined()
    expectSuccess = false
    btn.trigger('submit.prevent')

    // Expect component to trigger state actions
    expect(wrapper.vm.registrationCompleted).toBe(false)
    expect(wrapper.vm.registrationError).toBe(true)
    expect(wrapper.vm.registrationLoading).toBe(false)
    expect(wrapper.vm.errMsg).toBe(state.errMsg)

    // Expect Failure emission
    const emissions = wrapper.emitted().appAlert
    expect(emissions.length).toBe(1)
    const msg = 'An error occurred while processing your request: '
    expect(emissions[0][0]).toMatchObject(
      { 'msg': msg + state.errMsg, 'type': 'error' }
    )

    // Expect cleanup action
    expect(actions.clearRegistrationStatus).toHaveBeenCalled()
  })

  test('Does not attempt submission with invalid password length', () => {
    // Set valid data
    wrapper.setData({
      inputs: {
        username: invalidData1.username,
        password1: invalidData1.password1,
        password2: invalidData1.password2,
        email: invalidData1.email
      }
    })

    // Cause submission
    let btn = wrapper.find({ ref: 'registerForm' })
    expect(btn).toBeDefined()
    expectSuccess = false
    btn.trigger('submit.prevent')

    // Expect component to trigger state actions
    expect(wrapper.vm.registrationCompleted).toBe(false)
    expect(wrapper.vm.registrationError).toBe(false)
    expect(wrapper.vm.registrationLoading).toBe(false)
    expect(wrapper.vm.errMsg).toBe('')

    // Expect no emissions
    const emissions = wrapper.emitted().appAlert
    expect(emissions).toBeUndefined()

    // Expect cleanup action
    expect(actions.clearRegistrationStatus).not.toHaveBeenCalled()
  })

  test('Does not attempt submission with non-matching password1', () => {
    // Set valid data
    wrapper.setData({
      inputs: {
        username: invalidData2.username,
        password1: invalidData2.password1,
        password2: invalidData2.password2,
        email: invalidData2.email
      }
    })

    // Commenting out  for now, vue-test-utils cannot dirty input
    // to make this test work

    // // Cause submission
    // let btn = wrapper.find({ ref: 'registerForm' })
    // expect(btn).toBeDefined()
    // expectSuccess = false
    // btn.trigger('submit.prevent')

    // // Expect component to trigger state actions
    // expect(wrapper.vm.registrationCompleted).toBe(false)
    // expect(wrapper.vm.registrationError).toBe(false)
    // expect(wrapper.vm.registrationLoading).toBe(false)
    // expect(wrapper.vm.errMsg).toBe('')

    // // Expect no emissions
    // const emissions = wrapper.emitted().appAlert
    // expect(emissions).toBeUndefined()

    // // Expect cleanup action
    // expect(actions.clearRegistrationStatus).not.toHaveBeenCalled()
  })

  test('Does not attempt submission with non-matching password2', () => {
    // Set valid data
    wrapper.setData({
      inputs: {
        username: invalidData3.username,
        password1: invalidData3.password1,
        password2: invalidData3.password2,
        email: invalidData3.email
      }
    })

    // Commenting out  for now, vue-test-utils cannot dirty input
    // to make this test work

    // // Cause submission
    // let btn = wrapper.find({ ref: 'registerForm' })
    // expect(btn).toBeDefined()
    // expectSuccess = false
    // btn.trigger('submit.prevent')

    // // Expect component to trigger state actions
    // expect(wrapper.vm.registrationCompleted).toBe(false)
    // expect(wrapper.vm.registrationError).toBe(false)
    // expect(wrapper.vm.registrationLoading).toBe(false)
    // expect(wrapper.vm.errMsg).toBe('')

    // // Expect no emissions
    // const emissions = wrapper.emitted().appAlert
    // expect(emissions).toBeUndefined()

    // // Expect cleanup action
    // expect(actions.clearRegistrationStatus).not.toHaveBeenCalled()
  })

  test('Does not attempt submission with bad email input', () => {
    // Set valid data
    wrapper.setData({
      inputs: {
        username: invalidData4.username,
        password1: invalidData4.password1,
        password2: invalidData4.password2,
        email: invalidData4.email
      }
    })

    // Cause submission
    let btn = wrapper.find({ ref: 'registerForm' })
    expect(btn).toBeDefined()
    expectSuccess = false
    btn.trigger('submit.prevent')

    // Expect component to trigger state actions
    expect(wrapper.vm.registrationCompleted).toBe(false)
    expect(wrapper.vm.registrationError).toBe(false)
    expect(wrapper.vm.registrationLoading).toBe(false)
    expect(wrapper.vm.errMsg).toBe('')

    // Expect no emissions
    const emissions = wrapper.emitted().appAlert
    expect(emissions).toBeUndefined()

    // Expect cleanup action
    expect(actions.clearRegistrationStatus).not.toHaveBeenCalled()
  })
})
