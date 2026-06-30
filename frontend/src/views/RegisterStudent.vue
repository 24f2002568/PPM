<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card p-4 mt-4">
        <h3 class="mb-3 text-center">Student Registration</h3>
        <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
        <div v-if="success" class="alert alert-success py-2">{{ success }}</div>
        <form @submit.prevent="handleRegister">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Full Name</label>
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
              <label class="form-label">Contact</label>
              <input v-model="form.contact" class="form-control" />
            </div>
          </div>
          <div class="row">
            <div class="col-md-4 mb-3">
              <label class="form-label">Branch</label>
              <input v-model="form.branch" class="form-control" placeholder="e.g. CS" />
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">CGPA</label>
              <input v-model.number="form.cgpa" type="number" step="0.01" class="form-control" />
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Graduation Year</label>
              <input v-model.number="form.year" type="number" class="form-control" />
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Skills (comma separated)</label>
            <input v-model="form.skills" class="form-control" placeholder="Python, SQL, Flask" />
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
  name: '', email: '', password: '', contact: '', branch: '', cgpa: null, year: null, skills: '',
})

async function handleRegister() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await api.post('/auth/register/student', form)
    success.value = 'Registered successfully! Redirecting to login...'
    setTimeout(() => router.push('/login'), 1200)
  } catch (e) {
    error.value = e.response?.data?.error || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
