import { reactive } from 'vue'

const state = reactive({
  token: localStorage.getItem('ppa_token') || null,
  user: JSON.parse(localStorage.getItem('ppa_user') || 'null'),
})

function setAuth(token, user) {
  state.token = token
  state.user = user
  localStorage.setItem('ppa_token', token)
  localStorage.setItem('ppa_user', JSON.stringify(user))
}

function logout() {
  state.token = null
  state.user = null
  localStorage.removeItem('ppa_token')
  localStorage.removeItem('ppa_user')
}

function isLoggedIn() {
  return !!state.token
}

export const auth = { state, setAuth, logout, isLoggedIn }
