<template>
  <div class="row justify-content-center">
    <div class="col-md-7">
      <h3 class="mb-3">{{ isEdit ? 'Edit Job Posting' : 'Post New Job' }}</h3>
      <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
      <div v-if="success" class="alert alert-success py-2">{{ success }}</div>
      <div class="card p-4">
        <form @submit.prevent="submit">
          <div class="mb-3">
            <label class="form-label">Job Title</label>
            <input v-model="form.job_title" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Job Description</label>
            <textarea v-model="form.job_description" class="form-control" rows="3"></textarea>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Eligible Branches (comma separated, or "Any")</label>
              <input v-model="form.branch_eligibility" class="form-control" placeholder="CS, IT or Any" />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Min CGPA</label>
              <input v-model.number="form.min_cgpa" type="number" step="0.01" class="form-control" />
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Eligible Graduation Year (optional)</label>
              <input v-model.number="form.eligible_year" type="number" class="form-control" />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Salary</label>
              <input v-model="form.salary" class="form-control" placeholder="e.g. 8 LPA" />
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Skills Required (comma separated)</label>
            <input v-model="form.skills_required" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Application Deadline</label>
            <input v-model="form.application_deadline" type="date" class="form-control" />
          </div>
          <button class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? 'Saving...' : isEdit ? 'Save Changes' : 'Submit for Approval' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api/client'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const error = ref('')
const success = ref('')
const loading = ref(false)

const form = reactive({
  job_title: '', job_description: '', branch_eligibility: 'Any', min_cgpa: 0,
  eligible_year: null, salary: '', skills_required: '', application_deadline: '',
})

async function loadExisting() {
  if (!isEdit.value) return
  const { data } = await api.get('/company/drives')
  const drive = data.find((d) => d.id === Number(route.params.id))
  if (drive) {
    Object.assign(form, {
      job_title: drive.job_title,
      job_description: drive.job_description,
      branch_eligibility: drive.branch_eligibility,
      min_cgpa: drive.min_cgpa,
      eligible_year: drive.eligible_year,
      salary: drive.salary,
      skills_required: drive.skills_required,
      application_deadline: drive.application_deadline,
    })
  }
}

async function submit() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    if (isEdit.value) {
      await api.put(`/company/drives/${route.params.id}`, form)
      success.value = 'Updated successfully'
    } else {
      await api.post('/company/drives', form)
      success.value = 'Submitted for admin approval'
    }
    setTimeout(() => router.push('/company'), 1000)
  } catch (e) {
    error.value = e.response?.data?.error || 'Something went wrong'
  } finally {
    loading.value = false
  }
}

onMounted(loadExisting)
</script>
