<template>
  <div v-if="data.company">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>{{ data.company.name }} Dashboard</h3>
      <span class="badge" :class="data.company.approval_status === 'Approved' ? 'bg-success' : 'bg-warning text-dark'">
        {{ data.company.approval_status }}
      </span>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-4">
        <div class="card p-3 text-center">
          <div class="fs-3 fw-bold">{{ data.total_drives }}</div>
          <div class="text-muted small">Job Postings</div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card p-3 text-center">
          <div class="fs-3 fw-bold">{{ data.total_applicants }}</div>
          <div class="text-muted small">Total Applicants</div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card p-3 text-center d-flex justify-content-center">
          <router-link to="/company/drives/new" class="btn btn-primary">+ Post New Job</router-link>
        </div>
      </div>
    </div>

    <h5>Your Job Postings</h5>
    <table class="table bg-white">
      <thead>
        <tr><th>Title</th><th>Status</th><th>Deadline</th><th>Applicants</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-for="d in data.drives" :key="d.id">
          <td>{{ d.job_title }}</td>
          <td><span class="badge" :class="statusClass(d.status)">{{ d.status }}</span></td>
          <td>{{ d.application_deadline || '-' }}</td>
          <td>{{ d.applicant_count }}</td>
          <td class="d-flex gap-1">
            <router-link :to="`/company/drives/${d.id}/applicants`" class="btn btn-sm btn-outline-primary">
              View Applicants
            </router-link>
            <router-link :to="`/company/drives/${d.id}/edit`" class="btn btn-sm btn-outline-secondary">Edit</router-link>
            <button v-if="d.status === 'Approved'" class="btn btn-sm btn-outline-dark" @click="closeDrive(d.id)">Close</button>
          </td>
        </tr>
        <tr v-if="!data.drives?.length"><td colspan="5" class="text-center text-muted">No job postings yet</td></tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/client'

const data = ref({})

function statusClass(status) {
  return { Pending: 'bg-warning text-dark', Approved: 'bg-success', Rejected: 'bg-danger', Closed: 'bg-secondary' }[status] || 'bg-secondary'
}

async function load() {
  const { data: res } = await api.get('/company/dashboard')
  data.value = res
}

async function closeDrive(id) {
  await api.put(`/company/drives/${id}`, { status: 'Closed' })
  load()
}

onMounted(load)
</script>
