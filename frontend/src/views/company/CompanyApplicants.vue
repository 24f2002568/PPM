<template>
  <h3 class="mb-3">Applicants</h3>
  <table class="table bg-white">
    <thead>
      <tr><th>Student</th><th>Applied On</th><th>Status</th><th>Feedback</th><th></th></tr>
    </thead>
    <tbody>
      <tr v-for="a in applicants" :key="a.id">
        <td>{{ a.student_name }}</td>
        <td>{{ formatDate(a.application_date) }}</td>
        <td><span class="badge" :class="statusClass(a.status)">{{ a.status }}</span></td>
        <td>{{ a.feedback || '-' }}</td>
        <td>
          <select class="form-select form-select-sm" :value="a.status" @change="updateStatus(a, $event.target.value)">
            <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
          </select>
        </td>
      </tr>
      <tr v-if="!applicants.length"><td colspan="5" class="text-center text-muted">No applicants yet</td></tr>
    </tbody>
  </table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api/client'

const route = useRoute()
const applicants = ref([])
const statuses = ['Applied', 'Shortlisted', 'Interview', 'Offer', 'Rejected', 'Placed']

function statusClass(status) {
  return {
    Applied: 'bg-secondary', Shortlisted: 'bg-info text-dark', Interview: 'bg-primary',
    Offer: 'bg-success', Rejected: 'bg-danger', Placed: 'bg-success',
  }[status] || 'bg-secondary'
}

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString() : '-'
}

async function load() {
  const { data } = await api.get(`/company/drives/${route.params.id}/applicants`)
  applicants.value = data
}

async function updateStatus(application, status) {
  await api.put(`/company/applications/${application.id}`, { status })
  load()
}

onMounted(load)
</script>
