import session from './session'

// const rootAPI = process.env.VUE_APP_ROOT_API

export default {
  login (username, password) {
    return session.post('/auth/login/', { username, password })
  },
  logout () {
    return session.post('/auth/logout/', {})
  },
  createAccount (username, password1, password2, email) {
    return session.post(
      '/registration/', { username, password1, password2, email })
  },
  changeAccountPassword (oldPass, newPass) {
    return session.post('/auth/password/change/', { oldPass, newPass })
  },
  sendAccountPasswordResetEmail (email) {
    return session.post('/auth/password/reset/', { email })
  },
  resetAccountPassword (uid, token, newPass1, newPass2) {
    return session.post(
      '/auth/password/reset/confirm/', { uid, token, newPass1, newPass2 })
  },
  getAccountDetails () {
    return session.get('/auth/user/')
  },
  updateAccountDetails (data) {
    return session.patch('/auth/user/', data)
  },
  verifyAccountEmail (key) {
    return session.post('/registration/verify-email/', { key })
  },
  session
}
