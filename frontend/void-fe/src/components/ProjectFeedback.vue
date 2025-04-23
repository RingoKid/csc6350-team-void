<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  projectId: {
    type: [Number, String],
    required: true
  }
})

const feedbacks = ref([])
const newComment = ref('')
const isAuthenticated = ref(false)
const currentUsername = ref('')
const editingFeedbackId = ref(null)
const editedComment = ref('')
const error = ref(null)
const isLoading = ref(false)

onMounted(() => {
  isAuthenticated.value = !!localStorage.getItem('access_token')
  currentUsername.value = localStorage.getItem('username')
  fetchFeedback()
})

const fetchFeedback = async () => {
  try {
    isLoading.value = true
    const response = await fetch(`http://localhost:8000/api/projects/${props.projectId}/feedback/`)
    if (!response.ok) throw new Error('Failed to fetch feedback')
    feedbacks.value = await response.json()
  } catch (error) {
    console.error('Error fetching feedback:', error)
    error.value = error.message
  } finally {
    isLoading.value = false
  }
}

const refreshToken = async () => {
  try {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    const response = await fetch('http://localhost:8000/api/token/refresh/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        refresh: refreshToken
      })
    })

    if (!response.ok) {
      throw new Error('Failed to refresh token')
    }

    const data = await response.json()
    localStorage.setItem('access_token', data.access)
    return data.access
  } catch (error) {
    console.error('Error refreshing token:', error)
    // Clear tokens and redirect to login
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('username')
    window.dispatchEvent(new Event('auth-state-changed'))
    throw error
  }
}

const submitFeedback = async () => {
  if (!newComment.value.trim() || !isAuthenticated.value) return

  try {
    let token = localStorage.getItem('access_token')
    let response = await fetch(`http://localhost:8000/api/projects/${props.projectId}/feedback/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        project: props.projectId,
        comment: newComment.value
      })
    })

    // If token is expired, try to refresh it
    if (response.status === 401) {
      token = await refreshToken()
      // Retry the request with the new token
      response = await fetch(`http://localhost:8000/api/projects/${props.projectId}/feedback/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          project: props.projectId,
          comment: newComment.value
        })
      })
    }

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to submit feedback')
    }
    
    newComment.value = ''
    await fetchFeedback()
  } catch (error) {
    console.error('Error submitting feedback:', error)
    error.value = error.message
    if (error.message.includes('No refresh token available') || error.message.includes('Failed to refresh token')) {
      // Redirect to login if token refresh fails
      window.location.href = '/login'
    }
  }
}

const startEditing = (feedback) => {
  editingFeedbackId.value = feedback.id
  editedComment.value = feedback.comment
}

const cancelEditing = () => {
  editingFeedbackId.value = null
  editedComment.value = ''
}

const updateFeedback = async (feedbackId) => {
  if (!editedComment.value.trim()) return

  try {
    const response = await fetch(`http://localhost:8000/api/feedbacks/${feedbackId}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        project: props.projectId,
        comment: editedComment.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to update feedback')
    }
    
    editingFeedbackId.value = null
    editedComment.value = ''
    await fetchFeedback()
  } catch (error) {
    console.error('Error updating feedback:', error)
    error.value = error.message
  }
}

const deleteFeedback = async (feedbackId) => {
  if (!confirm('Are you sure you want to delete this feedback?')) return

  try {
    const response = await fetch(`http://localhost:8000/api/feedbacks/${feedbackId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })

    if (!response.ok) {
      throw new Error('Failed to delete feedback')
    }
    
    await fetchFeedback()
  } catch (error) {
    console.error('Error deleting feedback:', error)
    error.value = error.message
  }
}

const reportFeedback = async (feedbackId) => {
  const reason = prompt('Please provide a reason for reporting this feedback:')
  if (!reason) return

  try {
    const response = await fetch(`http://localhost:8000/api/reported-feedback/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        feedback_id: feedbackId,
        reason: reason
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to report feedback')
    }
    
    alert('Feedback reported successfully')
  } catch (error) {
    console.error('Error reporting feedback:', error)
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
  <div class="feedback-section">
    <h3>Feedback</h3>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="isLoading" class="loading">
      Loading feedback...
    </div>

    <div v-else>
      <!-- Feedback Input -->
      <div v-if="isAuthenticated" class="feedback-input">
        <textarea
          v-model="newComment"
          placeholder="Write your feedback..."
          rows="3"
        ></textarea>
        <button @click="submitFeedback" :disabled="!newComment.trim()">
          Submit Feedback
        </button>
      </div>
      <div v-else class="login-message">
        Please <router-link to="/login">login</router-link> to leave feedback
      </div>

      <!-- Feedback List -->
      <div class="feedback-list">
        <div v-for="feedback in feedbacks" :key="feedback.id" class="feedback-item">
          <div class="feedback-header">
            <span class="author">{{ feedback.user }}</span>
            <span class="date">
              {{ formatDate(feedback.created_at) }}
              <span v-if="feedback.updated_at !== feedback.created_at" class="edited-badge">(edited)</span>
            </span>
          </div>
          
          <div v-if="editingFeedbackId === feedback.id" class="edit-mode">
            <textarea v-model="editedComment" rows="3"></textarea>
            <div class="edit-actions">
              <button @click="updateFeedback(feedback.id)" :disabled="!editedComment.trim()">
                Save
              </button>
              <button @click="cancelEditing" class="cancel">
                Cancel
              </button>
            </div>
          </div>
          <div v-else class="feedback-content">
            <p>{{ feedback.comment }}</p>
            <div class="feedback-actions">
              <div v-if="feedback.user === currentUsername">
                <button @click="startEditing(feedback)" class="edit">
                  Edit
                </button>
                <button @click="deleteFeedback(feedback.id)" class="delete">
                  Delete
                </button>
              </div>
              <button v-else @click="reportFeedback(feedback.id)" class="report">
                Report
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="!feedbacks.length" class="no-feedback">
          No feedback yet
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.feedback-section {
  padding: 2rem;
  border-top: 1px solid #e5e7eb;
}

.feedback-section h3 {
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

.feedback-input {
  margin-bottom: 2rem;
}

.feedback-input textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 1rem;
  resize: vertical;
  font-family: inherit;
  font-size: 1rem;
  line-height: 1.5;
}

.feedback-input button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.feedback-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.feedback-input button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.login-message {
  text-align: center;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  color: #6b7280;
  margin-bottom: 2rem;
}

.login-message a {
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
}

.login-message a:hover {
  text-decoration: underline;
}

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feedback-item {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.author {
  font-weight: 600;
  color: #1f2937;
}

.date {
  color: #6b7280;
  font-size: 0.9rem;
}

.edited-badge {
  color: #9ca3af;
  font-size: 0.8rem;
  font-style: italic;
}

.edit-mode textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 1rem;
  resize: vertical;
  font-family: inherit;
  font-size: 1rem;
  line-height: 1.5;
}

.edit-actions {
  display: flex;
  gap: 1rem;
}

.edit-actions button {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-actions button:first-child {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
}

.edit-actions button:last-child {
  background: white;
  color: #6b7280;
  border: 1px solid #e5e7eb;
}

.edit-actions button:hover {
  transform: translateY(-2px);
}

.feedback-content {
  color: #4b5563;
  line-height: 1.6;
}

.feedback-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.feedback-actions button {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.feedback-actions .edit {
  background: white;
  color: #6366f1;
  border: 1px solid #6366f1;
}

.feedback-actions .delete {
  background: white;
  color: #ef4444;
  border: 1px solid #ef4444;
}

.feedback-actions button:hover {
  transform: translateY(-2px);
}

.feedback-actions .report {
  background: white;
  color: #f59e0b;
  border: 1px solid #f59e0b;
}

.feedback-actions .report:hover {
  background: #fef3c7;
}

.no-feedback {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
  background: #f9fafb;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .feedback-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .feedback-actions {
    flex-direction: column;
  }

  .feedback-actions button {
    width: 100%;
  }
}
</style> 