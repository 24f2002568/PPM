<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card p-4 mt-4">
        <h3 class="mb-3 text-center">Company Registration</h3>
        <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
        <div v-if="success" class="alert alert-success py-2">{{ success }}</div>
        <form @submit.prevent="handleRegister">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Company Name</label>
              <input v-model="form.name" class="form-control" required />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Email</label>
              <input v-model="form.email" type="email" class="form-control" required />
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-control" required />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Industry</label>
              <input v-model="form.industry" class="form-control" placeholder="e.g. IT Services" />
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">HR Contact</label>
              <input v-model="form.hr_contact" class="form-control" />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Website</label>
              <input v-model="form.website" class="form-control" placeholder="https://" />
            </div>
          </div>
          <button class="btn btn-primary w-100" type="submit" :disabled="loading">
            {{ loading ? 'Registering...' : 'Register' }}
          </button>
        </form>
        <p class="text-center mt-3 mb-0">
          <router-link to="/login">Already have an account? Login</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/client'

const router = useRouter()
const error = ref('')
const success = ref('')
const loading = ref(false)

const form = reactive({
  name: '', email: '', password: '', industry: '', hr_contact: '', website: '',
})

async function handleRegister() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    const { data } = await api.post('/auth/register/company', form)
    success.value = data.message
    setTimeout(() => router.push('/login'), 1800)
  } catch (e) {
    error.value = e.response?.data?.error || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
