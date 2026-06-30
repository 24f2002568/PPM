<template>
  <nav v-if="auth.isLoggedIn()" class="navbar navbar-expand navbar-dark bg-dark px-3">
    <span class="navbar-brand">PPA Portal</span>
    <div class="navbar-nav me-auto">
      <template v-if="role === 'admin'">
        <router-link class="nav-link" to="/admin">Dashboard</router-link>
        <router-link class="nav-link" to="/admin/companies">Companies</router-link>
        <router-link class="nav-link" to="/admin/students">Students</router-link>
        <router-link class="nav-link" to="/admin/drives">Drives</router-link>
      </template>
      <template v-else-if="role === 'company'">
        <router-link class="nav-link" to="/company">Dashboard</router-link>
        <router-link class="nav-link" to="/company/drives/new">Post Drive</router-link>
        <router-link class="nav-link" to="/company/profile">Profile</router-link>
      </template>
      <template v-else-if="role === 'student'">
        <router-link class="nav-link" to="/student">Dashboard</router-link>
        <router-link class="nav-link" to="/student/drives">Browse Drives</router-link>
        <router-link class="nav-link" to="/student/applications">My Applications</router-link>
        <router-link class="nav-link" to="/student/profile">Profile</router-link>
      </template>
    </div>
    <span class="navbar-text text-light me-3">{{ auth.state.user?.email }}</span>
    <button class="btn btn-outline-light btn-sm" @click="handleLogout">Logout</button>
  </nav>
  <div class="container py-4">
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from './store/auth'

const router = useRouter()
const role = computed(() => auth.state.user?.role)

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>
