<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import ReportedFeedbackPanel from '../components/ReportedFeedbackPanel.vue'

const isSuperuser = ref(false)

const checkSuperuserStatus = () => {
  const superuserStatus = localStorage.getItem('is_superuser') === 'true'
  console.log('Superuser status:', superuserStatus)
  isSuperuser.value = superuserStatus
}

onMounted(() => {
  checkSuperuserStatus()
  window.addEventListener('auth-state-changed', checkSuperuserStatus)
})

// Clean up event listener
onUnmounted(() => {
  window.removeEventListener('auth-state-changed', checkSuperuserStatus)
})
</script>

<template>
  <div class="dashboard">
    <div v-if="isSuperuser" class="admin-section">
      <h2>Admin Dashboard</h2>
      <ReportedFeedbackPanel />
    </div>
    <div v-else>
      <p>Welcome to your dashboard</p>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.admin-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

h2 {
  color: #1f2937;
  margin-bottom: 1.5rem;
}
</style> 