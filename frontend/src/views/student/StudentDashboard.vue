<template>
  <div v-if="data.student">
    <h3 class="mb-3">Welcome, {{ data.student.name }}</h3>
    <div class="row g-3 mb-4">
      <div class="col-md-4">
        <div class="card p-3 text-center">
          <div class="fs-3 fw-bold">{{ data.total_applications }}</div>
          <div class="text-muted small">Applications Submitted</div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card p-3 text-center d-flex justify-content-center">
          <router-link to="/student/drives" class="btn btn-primary">Browse Drives</router-link>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card p-3 text-center d-flex justify-content-center">
          <router-link to="/student/profile" class="btn btn-outline-secondary">Edit Profile</router-link>
        </div>
      </div>
    </div>

    <h5>Recent Applications</h5>
    <table class="table bg-white">
      <thead><tr><th>Company</th><th>Position</th><th>Status</th><th>Applied On</th></tr></thead>
      <tbody>
        <tr v-for="a in data.applications.slice(0, 5)" :key="a.id">
          <td>{{ a.company_name }}</td>
          <td>{{ a.job_title }}</td>
          <td><span class="badge" :class="statusClass(a.status)">{{ a.status }}</span></td>
          <td>{{ formatDate(a.application_date) }}</td>
        </tr>
        <tr v-if="!data.applications.length"><td colspan="4" class="text-center text-muted">No applications yet</td></tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/client'

const data = ref({ applications: [] })

function statusClass(status) {
  return {
    Applied: 'bg-secondary', Shortlisted: 'bg-info text-dark', Interview: 'bg-primary',
    Offer: 'bg-success', Rejected: 'bg-danger', Placed: 'bg-success',
  }[status] || 'bg-secondary'
}

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString() : '-'
}

onMounted(async () => {
  const { data: res } = await api.get('/student/dashboard')
  data.value = res
})
</script>
