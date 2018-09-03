import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

import store from './store'

Vue.use(Router)

const redirectLogout = (to, from, next) => {
  store.dispatch('auth/logout')
    .then(() => next('/login'))
}

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('./views/About.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('./views/Login.vue')
    },
    {
      path: '/logout',
      name: 'logout',
      beforeEnter: redirectLogout
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('./views/Register.vue')
    },
    {
      path: '/timebank',
      name: 'timebank',
      component: () => import('./views/TimeBank.vue')
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})

router.beforeEach((to, from, next) => {
  // Send user to login if not already signed in
  const publicPages = ['/login', '/register', '/', '/about', '/logout']
  const authRequired = !publicPages.includes(to.path)

  // Check authenticated status
  store.dispatch('auth/initialize')
    .then(() => {
      const loggedIn = store.getters['auth/isAuthenticated']
      if (authRequired && !loggedIn) {
        return next('/login')
      } else if (to.path === '/login' && loggedIn) {
        return next('/')
      }
    })
  next()
})

export default router
