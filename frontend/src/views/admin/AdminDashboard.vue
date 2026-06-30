<template>
  <h3 class="mb-4">Admin Dashboard</h3>
  <div v-if="loading" class="text-muted">Loading...</div>
  <div v-else class="row g-3">
    <div class="col-md-3" v-for="stat in stats" :key="stat.label">
      <div class="card p-3 text-center">
        <div class="fs-3 fw-bold">{{ stat.value }}</div>
        <div class="text-muted small">{{ stat.label }}</div>
      </div>
    </div>
  </div>

  <div class="row mt-4 g-3" v-if="!loading">
    <div class="col-md-6">
      <div class="card p-3">
        <h6>Pending Company Approvals: {{ data.pending_companies }}</h6>
        <router-link to="/admin/companies" class="btn btn-sm btn-outline-primary mt-2">
          Review Companies
        </router-link>
      </div>
    </div>
    <div class="col-md-6">
      <div class="card p-3">
        <h6>Pending Drive Approvals: {{ data.pending_drives }}</h6>
        <router-link to="/admin/drives" class="btn btn-sm btn-outline-primary mt-2">
          Review Drives
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api/client'

const loading = ref(true)
const data = ref({})

const stats = computed(() => [
  { label: 'Total Students', value: data.value.total_students ?? 0 },
  { label: 'Total Companies', value: data.value.total_companies ?? 0 },
  { label: 'Total Drives', value: data.value.total_drives ?? 0 },
  { label: 'Total Applications', value: data.value.total_applications ?? 0 },
])

onMounted(async () => {
  const { data: res } = await api.get('/admin/dashboard')
  data.value = res
  loading.value = false
})
</script>
