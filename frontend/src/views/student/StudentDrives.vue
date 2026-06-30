<template>
  <h3 class="mb-3">Browse Placement Drives</h3>
  <input v-model="search" @input="load" class="form-control mb-3" placeholder="Search by company, title, or skills..." />

  <div v-if="message" class="alert" :class="messageClass">{{ message }}</div>

  <div class="row g-3">
    <div class="col-md-6" v-for="d in drives" :key="d.id">
      <div class="card p-3">
        <div class="d-flex justify-content-between">
          <h5>{{ d.job_title }}</h5>
          <span class="text-muted small">{{ d.company_name }}</span>
        </div>
        <p class="mb-1 small text-muted">{{ d.job_description || 'No description provided.' }}</p>
        <p class="mb-1 small">
          <strong>Eligibility:</strong> {{ d.branch_eligibility }} | Min CGPA: {{ d.min_cgpa }}
          <span v-if="d.eligible_year"> | Grad Year: {{ d.eligible_year }}</span>
        </p>
        <p class="mb-1 small"><strong>Skills:</strong> {{ d.skills_required || '-' }}</p>
        <p class="mb-2 small"><strong>Salary:</strong> {{ d.salary || '-' }} | <strong>Deadline:</strong> {{ d.application_deadline || '-' }}</p>
        <button class="btn btn-sm btn-primary" :disabled="applying === d.id" @click="apply(d.id)">
          {{ applying === d.id ? 'Applying...' : 'Apply' }}
        </button>
      </div>
    </div>
    <div v-if="!drives.length" class="text-muted text-center">No approved drives found</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/client'

const drives = ref([])
const search = ref('')
const applying = ref(null)
const message = ref('')
const messageClass = ref('alert-success')

async function load() {
  const { data } = await api.get('/drives', { params: { search: search.value } })
  drives.value = data
}

async function apply(driveId) {
  applying.value = driveId
  message.value = ''
  try {
    await api.post(`/student/drives/${driveId}/apply`)
    message.value = 'Application submitted successfully!'
    messageClass.value = 'alert-success'
  } catch (e) {
    message.value = e.response?.data?.error || 'Could not apply'
    messageClass.value = 'alert-danger'
  } finally {
    applying.value = null
  }
}

onMounted(load)
</script>
