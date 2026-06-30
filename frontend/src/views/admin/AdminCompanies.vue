<template>
  <h3 class="mb-3">Companies</h3>
  <input v-model="search" @input="load" class="form-control mb-3" placeholder="Search by name or industry..." />

  <table class="table bg-white">
    <thead>
      <tr>
        <th>Name</th><th>Industry</th><th>Email</th><th>Status</th><th>Active</th><th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="c in companies" :key="c.id">
        <td>{{ c.name }}</td>
        <td>{{ c.industry || '-' }}</td>
        <td>{{ c.email }}</td>
        <td>
          <span class="badge" :class="statusClass(c.approval_status)">{{ c.approval_status }}</span>
        </td>
        <td>
          <span class="badge" :class="c.is_active ? 'bg-success' : 'bg-secondary'">
            {{ c.is_active ? 'Active' : 'Deactivated' }}
          </span>
        </td>
        <td class="d-flex gap-1">
          <button v-if="c.approval_status === 'Pending'" class="btn btn-sm btn-success" @click="approve(c.id)">Approve</button>
          <button v-if="c.approval_status === 'Pending'" class="btn btn-sm btn-outline-danger" @click="reject(c.id)">Reject</button>
          <button class="btn btn-sm btn-outline-secondary" @click="toggleActive(c.id)">
            {{ c.is_active ? 'Deactivate' : 'Activate' }}
          </button>
          <button class="btn btn-sm btn-outline-danger" @click="remove(c.id)">Remove</button>
        </td>
      </tr>
      <tr v-if="!companies.length"><td colspan="6" class="text-center text-muted">No companies found</td></tr>
    </tbody>
  </table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/client'

const companies = ref([])
const search = ref('')

function statusClass(status) {
  return { Pending: 'bg-warning text-dark', Approved: 'bg-success', Rejected: 'bg-danger' }[status] || 'bg-secondary'
}

async function load() {
  const { data } = await api.get('/admin/companies', { params: { search: search.value } })
  companies.value = data
}

async function approve(id) {
  await api.post(`/admin/companies/${id}/approve`)
  load()
}
async function reject(id) {
  await api.post(`/admin/companies/${id}/reject`)
  load()
}
async function toggleActive(id) {
  await api.post(`/admin/companies/${id}/toggle-active`)
  load()
}
async function remove(id) {
  if (!confirm('Remove this company permanently?')) return
  await api.delete(`/admin/companies/${id}`)
  load()
}

onMounted(load)
</script>
