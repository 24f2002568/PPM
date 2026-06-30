<template>
  <h3 class="mb-3">Students</h3>
  <input v-model="search" @input="load" class="form-control mb-3" placeholder="Search by name, contact, or email..." />

  <table class="table bg-white">
    <thead>
      <tr><th>Name</th><th>Branch</th><th>CGPA</th><th>Year</th><th>Email</th><th>Active</th><th></th></tr>
    </thead>
    <tbody>
      <tr v-for="s in students" :key="s.id">
        <td>{{ s.name }}</td>
        <td>{{ s.branch || '-' }}</td>
        <td>{{ s.cgpa ?? '-' }}</td>
        <td>{{ s.year ?? '-' }}</td>
        <td>{{ s.email }}</td>
        <td>
          <span class="badge" :class="s.is_active ? 'bg-success' : 'bg-secondary'">
            {{ s.is_active ? 'Active' : 'Deactivated' }}
          </span>
        </td>
        <td>
          <button class="btn btn-sm btn-outline-secondary" @click="toggleActive(s.id)">
            {{ s.is_active ? 'Deactivate' : 'Activate' }}
          </button>
        </td>
      </tr>
      <tr v-if="!students.length"><td colspan="7" class="text-center text-muted">No students found</td></tr>
    </tbody>
  </table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/client'

const students = ref([])
const search = ref('')

async function load() {
  const { data } = await api.get('/admin/students', { params: { search: search.value } })
  students.value = data
}

async function toggleActive(id) {
  await api.post(`/admin/students/${id}/toggle-active`)
  load()
}

onMounted(load)
</script>
