<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <h3 class="mb-3">Company Profile</h3>
      <div v-if="success" class="alert alert-success py-2">{{ success }}</div>
      <div class="card p-4">
        <form @submit.prevent="save">
          <div class="mb-3">
            <label class="form-label">Company Name</label>
            <input v-model="form.name" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Industry</label>
            <input v-model="form.industry" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">HR Contact</label>
            <input v-model="form.hr_contact" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Website</label>
            <input v-model="form.website" class="form-control" />
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
const form = reactive({ name: '', industry: '', hr_contact: '', website: '' })

async function load() {
  const { data } = await api.get('/company/profile')
  Object.assign(form, data)
}

async function save() {
  loading.value = true
  success.value = ''
  try {
    await api.put('/company/profile', form)
    success.value = 'Profile updated'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
