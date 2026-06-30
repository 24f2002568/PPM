<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <h3 class="mb-3">My Profile</h3>
      <div v-if="success" class="alert alert-success py-2">{{ success }}</div>
      <div class="card p-4">
        <form @submit.prevent="save">
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input v-model="form.name" class="form-control" required />
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Branch</label>
              <input v-model="form.branch" class="form-control" />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Contact</label>
              <input v-model="form.contact" class="form-control" />
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">CGPA</label>
              <input v-model.number="form.cgpa" type="number" step="0.01" class="form-control" />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Graduation Year</label>
              <input v-model.number="form.year" type="number" class="form-control" />
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Skills (comma separated)</label>
            <input v-model="form.skills" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Resume Filename</label>
            <input v-model="form.resume_filename" class="form-control" placeholder="resume.pdf" />
            <div class="form-text">File upload not required for this milestone — just track the filename.</div>
          </div>
          <button class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? 'Saving...' : 'Save Changes' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../../api/client'

const success = ref('')
const loading = ref(false)
const form = reactive({ name: '', branch: '', contact: '', cgpa: null, year: null, skills: '', resume_filename: '' })

async function load() {
  const { data } = await api.get('/student/profile')
  Object.assign(form, data)
}

async function save() {
  loading.value = true
  success.value = ''
  try {
    await api.put('/student/profile', form)
    success.value = 'Profile updated'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
