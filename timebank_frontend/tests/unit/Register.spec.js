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

  const validData = {
    username: 'TEST',
    password1: 'qweasdzx',
    password2: 'qweasdzx',
    email: 'test@example.com'
  }
  const invalidData = {
    username: 'TEST',
    password1: 'qweasdz',
    password2: 'qweasdz',
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

    actions = {
      createAccount: function () {state.registrationCompleted = true},
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

  test('Calls createAccount on user submit', () => {
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
    btn.trigger('submit.prevent')

    // Expect component to trigger state actions
    expect(wrapper.vm.registrationCompleted).toBe(true)

    // Expect success emission
    const emissions = wrapper.emitted().appAlert
    expect(emissions.length).toBe(1)
    const msg = 'Registration complete, check your email\n'
    expect(emissions[0][0]).toMatchObject({'msg': msg, 'type': 'success'})

    // Expect cleanup action
    expect(actions.clearRegistrationStatus).toHaveBeenCalled()
  })
})
