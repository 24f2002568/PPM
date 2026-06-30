<template>
  <h3 class="mb-3">Placement Drives</h3>
  <table class="table bg-white">
    <thead>
      <tr><th>Title</th><th>Company</th><th>Deadline</th><th>Status</th><th>Applicants</th><th></th></tr>
    </thead>
    <tbody>
      <tr v-for="d in drives" :key="d.id">
        <td>{{ d.job_title }}</td>
        <td>{{ d.company_name }}</td>
        <td>{{ d.application_deadline || '-' }}</td>
        <td><span class="badge" :class="statusClass(d.status)">{{ d.status }}</span></td>
        <td>{{ d.applicant_count }}</td>
        <td class="d-flex gap-1">
          <button v-if="d.status === 'Pending'" class="btn btn-sm btn-success" @click="approve(d.id)">Approve</button>
          <button v-if="d.status === 'Pending'" class="btn btn-sm btn-outline-danger" @click="reject(d.id)">Reject</button>
          <button class="btn btn-sm btn-outline-danger" @click="remove(d.id)">Remove</button>
        </td>
      </tr>
      <tr v-if="!drives.length"><td colspan="6" class="text-center text-muted">No drives found</td></tr>
    </tbody>
  </table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/client'

const drives = ref([])

function statusClass(status) {
  return { Pending: 'bg-warning text-dark', Approved: 'bg-success', Rejected: 'bg-danger', Closed: 'bg-secondary' }[status] || 'bg-secondary'
}

async function load() {
  const { data } = await api.get('/admin/drives')
  drives.value = data
}

async function approve(id) {
  await api.post(`/admin/drives/${id}/approve`)
  load()
}
async function reject(id) {
  await api.post(`/admin/drives/${id}/reject`)
  load()
}
async function remove(id) {
  if (!confirm('Remove this drive permanently?')) return
  await api.delete(`/admin/drives/${id}`)
  load()
}

onMounted(load)
</script>
