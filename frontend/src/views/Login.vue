<template>
  <div class="row justify-content-center">
    <div class="col-md-5">
      <div class="card p-4 mt-5">
        <h3 class="mb-3 text-center">Login</h3>
        <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" required />
          </div>
          <button class="btn btn-primary w-100" type="submit" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        <hr />
        <p class="text-center mb-1">New here?</p>
        <div class="d-flex gap-2">
          <router-link to="/register/student" class="btn btn-outline-secondary btn-sm w-50">
            Register as Student
          </router-link>
          <router-link to="/register/company" class="btn btn-outline-secondary btn-sm w-50">
            Register as Company
          </router-link>
        </div>
        <p class="text-muted small mt-3 mb-0 text-center">Admin login: admin@ppa.com / admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/client'
import { auth } from '../store/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const { data } = await api.post('/auth/login', { email: email.value, password: password.value })
    auth.setAuth(data.token, data.user)
    router.push(`/${data.user.role}`)
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
