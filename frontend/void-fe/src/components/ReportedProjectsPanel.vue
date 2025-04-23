<script setup>
import { ref, onMounted } from 'vue'

const reportedProjects = ref([])
const error = ref(null)
const isLoading = ref(false)

onMounted(() => {
  fetchReportedProjects()
})

const fetchReportedProjects = async () => {
  try {
    isLoading.value = true
    const token = localStorage.getItem('access_token')
    console.log('Fetching reported projects with token:', token ? 'Present' : 'Missing')
    
    const response = await fetch('http://localhost:8000/api/reported-projects/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    console.log('Response status:', response.status)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      console.error('API Error:', errorData)
      throw new Error(errorData.detail || `Failed to fetch reported projects: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('Fetched reported projects:', data)
    reportedProjects.value = data
  } catch (err) {
    console.error('Error fetching reported projects:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

const resolveReport = async (reportId) => {
  try {
    const response = await fetch(`http://localhost:8000/api/reported-projects/${reportId}/resolve/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      console.error('Resolve report error:', errorData)
      throw new Error(errorData.detail || `Failed to resolve report: ${response.status}`)
    }
    
    await fetchReportedProjects()
  } catch (error) {
    console.error('Error resolving report:', error)
    error.value = error.message
  }
}

const deleteProject = async (reportId) => {
  if (!confirm('Are you sure you want to delete this project? This action cannot be undone.')) return

  try {
    const response = await fetch(`http://localhost:8000/api/reported-projects/${reportId}/delete_project/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      console.error('Delete project error:', errorData)
      throw new Error(errorData.detail || `Failed to delete project: ${response.status}`)
    }
    
    await fetchReportedProjects()
  } catch (error) {
    console.error('Error deleting project:', error)
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
  <div class="reported-projects-panel">
    <h2>Reported Projects</h2>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>Loading reported projects...</p>
    </div>

    <div v-else-if="reportedProjects.length === 0" class="no-reports">
      <p>No reported projects</p>
    </div>

    <div v-else class="reported-projects-list">
      <div v-for="report in reportedProjects" :key="report.id" class="report-card">
        <div class="report-header">
          <h3>
            <router-link :to="{ name: 'SinglePageView', params: { id: report.project.id }}" class="project-link">
              {{ report.project.title }}
            </router-link>
          </h3>
          <span class="report-status" :class="{ 'resolved': report.is_resolved }">
            {{ report.is_resolved ? 'Resolved' : 'Pending' }}
          </span>
        </div>
        <div class="report-details">
          <p class="report-reason">{{ report.reason }}</p>
          <div class="report-meta">
            <span>Reported by: {{ report.reporter }}</span>
            <span>Date: {{ formatDate(report.created_at) }}</span>
          </div>
          <div v-if="report.is_resolved" class="resolution-details">
            <span>Resolved by: {{ report.resolved_by }}</span>
            <span>Date: {{ formatDate(report.resolved_at) }}</span>
          </div>
        </div>
        <div class="report-actions">
          <button 
            v-if="!report.is_resolved" 
            @click="resolveReport(report.id)" 
            class="resolve-btn"
            :disabled="isResolving"
          >
            Resolve Report
          </button>
          <button 
            v-if="!report.is_resolved" 
            @click="deleteProject(report.id)" 
            class="delete-btn"
            :disabled="isDeleting"
          >
            Delete Project
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reported-projects-panel {
  padding: 2rem;
}

.reported-projects-panel h2 {
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

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  border: 3px solid #f3f4f6;
  border-top: 3px solid #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-reports {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
  background: #f9fafb;
  border-radius: 8px;
}

.reported-projects-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.report-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.project-link {
  color: #1f2937;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.project-link:hover {
  color: #6366f1;
}

.report-status {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.report-status:not(.resolved) {
  background: #fee2e2;
  color: #ef4444;
}

.report-status.resolved {
  background: #dcfce7;
  color: #22c55e;
}

.report-details {
  margin-bottom: 1rem;
}

.report-reason {
  color: #4b5563;
  margin-bottom: 0.5rem;
}

.report-meta, .resolution-details {
  display: flex;
  gap: 1rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.report-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.resolve-btn, .delete-btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.resolve-btn {
  background: #dcfce7;
  color: #22c55e;
  border: 1px solid #22c55e;
}

.delete-btn {
  background: #fee2e2;
  color: #ef4444;
  border: 1px solid #ef4444;
}

.resolve-btn:hover:not(:disabled), .delete-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.resolve-btn:disabled, .delete-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .reported-projects-panel {
    padding: 1rem;
  }

  .report-meta, .resolution-details {
    flex-direction: column;
    gap: 0.5rem;
  }

  .report-actions {
    flex-direction: column;
  }
}
</style> 