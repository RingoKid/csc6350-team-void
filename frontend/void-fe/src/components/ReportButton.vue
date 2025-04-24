<template>
  <button 
    class="report-button"
    @click="handleReport"
    :disabled="isReporting"
  >
    <span v-if="isReporting">Reporting...</span>
    <span v-else>Report Project</span>
  </button>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  }
})

const isReporting = ref(false)

const handleReport = async () => {
  const reason = prompt('Please provide a reason for reporting this project:')
  if (!reason) return

  try {
    isReporting.value = true
    const response = await fetch('http://localhost:8000/api/reported-projects/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        project_id: props.projectId,
        reason: reason
      })
    })

    if (!response.ok) {
      throw new Error('Failed to report project')
    }

    alert('Project reported successfully. Thank you for your feedback.')
  } catch (error) {
    console.error('Error reporting project:', error)
    alert('Failed to report project. Please try again later.')
  } finally {
    isReporting.value = false
  }
}
</script>

<style scoped>
.report-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  background: white;
  color: #ef4444;
  border: 1px solid #ef4444;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.report-button:hover:not(:disabled) {
  background: #fee2e2;
  transform: translateY(-2px);
}

.report-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style> 