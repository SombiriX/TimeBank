import { expect } from 'chai'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
// import '../../src/plugins/vuetify'
import Vuetify from 'vuetify'
import sinon from 'sinon'
import Register from '@/views/Register.vue'

describe('Register.vue', function () {
  // Mock up some testing functions and data
  let wrapper
  let actions
  let modules
  let signup
  let state
  let store

  const routes = [
    { path: '/login', name: 'login' }
  ]
  const router = new VueRouter({ routes })

  beforeEach(function () {
    const localVue = createLocalVue()
    localVue.use(Vuex)
    localVue.use(VueRouter)
    localVue.use(Vuetify)

    state = {
      registrationCompleted: false,
      registrationError: false,
      registrationLoading: false,
      errMsg: ''
    }

    actions = {
      createAccount: sinon.stub(),
      clearRegistrationStatus: sinon.stub()
    }

    signup = {
      namespaced: true,
      state,
      actions
    }

    modules = { signup }

    store = new Vuex.Store({ modules })

    wrapper = shallowMount(Register, {
      localVue: localVue,
      store,
      router
    })
  })

  it('Emits success alert on valid user creation', function () {
    // Set valid data
    // wrapper.setData({
    //   inputs: {
    //     username: validData.username,
    //     password1: validData.password1,
    //     password2: validData.password2,
    //     email: validData.email
    //   }
    // })

    // Cause submission
    let btn = wrapper.find({ ref: 'registerForm' })
    let inputs = wrapper.findAll('input')
    console.log('[inputs]', wrapper.html())
    expect(btn).to.exist
    btn.trigger('submit.prevent')

    // Expect component to trigger state actions
    // expect(fnStatus.createAccount).to.be.true
    expect(actions.createAccount.calledOnce).to.be.true

    // State response should occur automatically with mocked functions

    // Expect success emission
    const emmisssions = wrapper.emitted().appAlert
    expect(emmisssions.length).to.equal(1 + 1)
    expect(emmisssions[0][0]).to.have.all.keys('msg', 'type')

    // Expect cleanup action
    expect(actions.signup.clearRegistrationStatus).toHaveBeenCalled()
  })
})
