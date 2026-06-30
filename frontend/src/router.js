import { createRouter, createWebHistory } from 'vue-router'
import { auth } from './store/auth'

import Login from './views/Login.vue'
import RegisterStudent from './views/RegisterStudent.vue'
import RegisterCompany from './views/RegisterCompany.vue'

import AdminDashboard from './views/admin/AdminDashboard.vue'
import AdminCompanies from './views/admin/AdminCompanies.vue'
import AdminStudents from './views/admin/AdminStudents.vue'
import AdminDrives from './views/admin/AdminDrives.vue'

import CompanyDashboard from './views/company/CompanyDashboard.vue'
import CompanyDriveForm from './views/company/CompanyDriveForm.vue'
import CompanyApplicants from './views/company/CompanyApplicants.vue'
import CompanyProfile from './views/company/CompanyProfile.vue'

import StudentDashboard from './views/student/StudentDashboard.vue'
import StudentDrives from './views/student/StudentDrives.vue'
import StudentApplications from './views/student/StudentApplications.vue'
import StudentProfile from './views/student/StudentProfile.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login, meta: { public: true } },
  { path: '/register/student', component: RegisterStudent, meta: { public: true } },
  { path: '/register/company', component: RegisterCompany, meta: { public: true } },

  { path: '/admin', component: AdminDashboard, meta: { role: 'admin' } },
  { path: '/admin/companies', component: AdminCompanies, meta: { role: 'admin' } },
  { path: '/admin/students', component: AdminStudents, meta: { role: 'admin' } },
  { path: '/admin/drives', component: AdminDrives, meta: { role: 'admin' } },

  { path: '/company', component: CompanyDashboard, meta: { role: 'company' } },
  { path: '/company/profile', component: CompanyProfile, meta: { role: 'company' } },
  { path: '/company/drives/new', component: CompanyDriveForm, meta: { role: 'company' } },
  { path: '/company/drives/:id/edit', component: CompanyDriveForm, meta: { role: 'company' } },
  { path: '/company/drives/:id/applicants', component: CompanyApplicants, meta: { role: 'company' } },

  { path: '/student', component: StudentDashboard, meta: { role: 'student' } },
  { path: '/student/drives', component: StudentDrives, meta: { role: 'student' } },
  { path: '/student/applications', component: StudentApplications, meta: { role: 'student' } },
  { path: '/student/profile', component: StudentProfile, meta: { role: 'student' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.meta.public) {
    return next()
  }
  if (!auth.isLoggedIn()) {
    return next('/login')
  }
  if (to.meta.role && auth.state.user?.role !== to.meta.role) {
    return next(`/${auth.state.user?.role}`)
  }
  next()
})

export default router
