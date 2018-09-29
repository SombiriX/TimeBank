import { expect } from 'chai'
import { mount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import '../../src/plugins/vuetify'
import sinon from 'sinon'
import Register from '@/views/Register.vue'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(VueRouter)

describe('Register.vue', function () {
  // Mock up some testing functions and data
  let actions
  let state
  let store

  // Stores whether each function has been called
  let fnStatus = {
    createAccount: false,
    clearRegistrationStatus: false
  }

  // Mock Vuex functions
  let createInput
  function setStateSuccess (state) {
    state.registrationCompleted = true
  }
  function setStateFail (state) {
    state.registrationError = true
  }
  function createFnSuccess ({ commit }, input) {
    console.log('[createFnSuccess]', this)
    fnStatus.createAccount = true
    createInput = { ...input }
    commit(setStateSuccess)
  }
  function createFnFail ({ commit }, input) {
    fnStatus.createAccount = true
    createInput = { ...input }
    commit(setStateFail)
  }

  function clearFn () {
    fnStatus.clearRegistrationStatus = true
  }

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

  beforeEach(function () {
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

    store = new Vuex.Store({
      modules: {
        signup: {
          namespaced: true,
          state: state,
          actions: actions
        }
      }
    })
  })

  it('Emits success alert on valid user creation', function () {
    const wrapper = mount(Register, { store, localVue })
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
    let btn = wrapper.find({ ref: 'createAccBtn' })
    expect(btn).to.exist
    btn.trigger('click')

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
