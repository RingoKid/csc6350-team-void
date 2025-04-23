<script setup>
import { ref, onMounted } from 'vue'

const reportedFeedback = ref([])
const error = ref(null)
const isLoading = ref(false)

onMounted(() => {
  fetchReportedFeedback()
})

const fetchReportedFeedback = async () => {
  try {
    isLoading.value = true
    const token = localStorage.getItem('access_token')
    console.log('Fetching reported feedback with token:', token ? 'Present' : 'Missing')
    console.log('Is superuser:', localStorage.getItem('is_superuser'))
    
    const response = await fetch('http://localhost:8000/api/reported-feedback/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    console.log('Response status:', response.status)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      console.error('API Error:', errorData)
      throw new Error(errorData.detail || `Failed to fetch reported feedback: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('Fetched reported feedback:', data)
    reportedFeedback.value = data
  } catch (err) {
    console.error('Error fetching reported feedback:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

const resolveReport = async (reportId) => {
  try {
    const response = await fetch(`http://localhost:8000/api/reported-feedback/${reportId}/resolve/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    if (!response.ok) throw new Error('Failed to resolve report')
    await fetchReportedFeedback()
  } catch (error) {
    console.error('Error resolving report:', error)
    error.value = error.message
  }
}

const deleteFeedback = async (reportId) => {
  if (!confirm('Are you sure you want to delete this feedback?')) return

  try {
    const response = await fetch(`http://localhost:8000/api/reported-feedback/${reportId}/delete_feedback/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      console.error('Delete feedback error:', errorData)
      throw new Error(errorData.detail || `Failed to delete feedback: ${response.status}`)
    }
    
    await fetchReportedFeedback()
  } catch (error) {
    console.error('Error deleting feedback:', error)
    error.value = error.message
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="reported-feedback-panel">
    <h2>Reported Feedback</h2>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="isLoading" class="loading">
      Loading reported feedback...
    </div>

    <div v-else>
      <div v-if="reportedFeedback.length" class="reports-list">
        <div v-for="report in reportedFeedback" :key="report.id" class="report-item">
          <div class="report-header">
            <div class="feedback-info">
              <span class="author">{{ report.feedback.user }}</span>
              <span class="date">{{ formatDate(report.feedback.created_at) }}</span>
            </div>
            <div class="report-info">
              <span class="reporter">Reported by: {{ report.reporter }}</span>
              <span class="report-date">{{ formatDate(report.created_at) }}</span>
              <span class="report-status" :class="{ 'resolved': report.is_resolved }">
                {{ report.is_resolved ? 'Resolved' : 'Pending' }}
              </span>
            </div>
          </div>
          
          <div class="feedback-content">
            <p>{{ report.feedback.comment }}</p>
          </div>
          
          <div class="report-reason">
            <strong>Reason:</strong>
            <p>{{ report.reason }}</p>
          </div>

          <div v-if="report.is_resolved" class="resolution-details">
            <span>Resolved by: {{ report.resolved_by }}</span>
            <span>Date: {{ formatDate(report.resolved_at) }}</span>
          </div>
          
          <div v-if="!report.is_resolved" class="report-actions">
            <button @click="resolveReport(report.id)" class="resolve">
              Mark as Resolved
            </button>
            <button @click="deleteFeedback(report.id)" class="delete">
              Delete Feedback
            </button>
          </div>
        </div>
      </div>
      <div v-else class="no-reports">
        No reported feedback
      </div>
    </div>
  </div>
</template>

<style scoped>
.reported-feedback-panel {
  padding: 2rem;
}

.reported-feedback-panel h2 {
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.error-message {
  background-color: #fee2e2;
  color: #ef4444;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.report-item {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.report-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.feedback-info, .report-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.author, .reporter {
  font-weight: 600;
  color: #1f2937;
}

.date, .report-date {
  color: #6b7280;
  font-size: 0.9rem;
}

.report-status {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  align-self: flex-start;
}

.report-status:not(.resolved) {
  background: #fee2e2;
  color: #ef4444;
}

.report-status.resolved {
  background: #dcfce7;
  color: #22c55e;
}

.feedback-content {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
}

.report-reason {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #fef3c7;
  border-radius: 6px;
}

.report-reason strong {
  color: #92400e;
  display: block;
  margin-bottom: 0.5rem;
}

.report-reason p {
  color: #78350f;
  line-height: 1.6;
}

.resolution-details {
  display: flex;
  gap: 1rem;
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f3f4f6;
  border-radius: 6px;
}

.report-actions {
  display: flex;
  gap: 1rem;
}

.report-actions button {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.report-actions .resolve {
  background: white;
  color: #10b981;
  border: 1px solid #10b981;
}

.report-actions .delete {
  background: white;
  color: #ef4444;
  border: 1px solid #ef4444;
}

.report-actions button:hover {
  transform: translateY(-2px);
}

.no-reports {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
  background: #f9fafb;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .report-header {
    flex-direction: column;
    gap: 1rem;
  }

  .report-actions {
    flex-direction: column;
  }

  .report-actions button {
    width: 100%;
  }
}
</style> 