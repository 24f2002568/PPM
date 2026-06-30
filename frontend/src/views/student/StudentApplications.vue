<template>
  <h3 class="mb-3">My Applications</h3>
  <table class="table bg-white">
    <thead>
      <tr><th>Company</th><th>Position</th><th>Applied On</th><th>Status</th><th>Interview</th><th>Feedback</th></tr>
    </thead>
    <tbody>
      <tr v-for="a in applications" :key="a.id">
        <td>{{ a.company_name }}</td>
        <td>{{ a.job_title }}</td>
        <td>{{ formatDate(a.application_date) }}</td>
        <td><span class="badge" :class="statusClass(a.status)">{{ a.status }}</span></td>
        <td>{{ a.interview_datetime ? new Date(a.interview_datetime).toLocaleString() : '-' }}</td>
        <td>{{ a.feedback || '-' }}</td>
      </tr>
      <tr v-if="!applications.length"><td colspan="6" class="text-center text-muted">No applications yet</td></tr>
    </tbody>
  </table>

  <h3 class="mt-5 mb-3">Placement History</h3>
  <table class="table bg-white">
    <thead><tr><th>Position</th><th>Salary</th><th>Joining Date</th></tr></thead>
    <tbody>
      <tr v-for="p in placements" :key="p.id">
        <td>{{ p.position }}</td>
        <td>{{ p.salary || '-' }}</td>
        <td>{{ p.joining_date || 'To be confirmed' }}</td>
      </tr>
      <tr v-if="!placements.length"><td colspan="3" class="text-center text-muted">No placements yet</td></tr>
    </tbody>
  </table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/client'

const applications = ref([])
const placements = ref([])

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
  const [appsRes, placementsRes] = await Promise.all([
    api.get('/student/applications'),
    api.get('/student/placements'),
  ])
  applications.value = appsRes.data
  placements.value = placementsRes.data
})
</script>
