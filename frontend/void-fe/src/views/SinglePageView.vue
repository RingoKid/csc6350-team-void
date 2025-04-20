<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import StarRating from '../components/StarRating.vue'

const route = useRoute()
const project = ref(null)
const error = ref(null)
const feedbacks = ref([])
const newComment = ref('')
const isAuthenticated = ref(false)
const currentUsername = ref('')

onMounted(() => {
  isAuthenticated.value = !!localStorage.getItem('access_token')
  currentUsername.value = localStorage.getItem('username')
  fetchProject()
  fetchFeedback()
})

const isProjectOwner = computed(() => {
  console.log('Current username:', currentUsername.value)
  console.log('Project user:', project.value?.user)
  return project.value && project.value.user === currentUsername.value
})

const fetchProject = async () => {
  try {
    const response = await fetch(`http://localhost:8000/api/projects/${route.params.id}/`)
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to fetch project')
    }
    const data = await response.json()
    project.value = data
    console.log('Project data:', data)
    console.log('Is owner?', isProjectOwner.value)
  } catch (error) {
    console.error('Error fetching project:', error)
    error.value = error.message
  }
}

const fetchFeedback = async () => {
  try {
    const response = await fetch(`http://localhost:8000/api/projects/${route.params.id}/feedback/`)
    if (!response.ok) throw new Error('Failed to fetch feedback')
    feedbacks.value = await response.json()
  } catch (error) {
    console.error('Error fetching feedback:', error)
  }
}

const handleRatingUpdated = async () => {
  await fetchProject()
}

const submitFeedback = async () => {
  if (!newComment.value.trim() || !isAuthenticated.value) return

  try {
    const response = await fetch(`http://localhost:8000/api/feedbacks/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        project: route.params.id,
        comment: newComment.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to submit feedback')
    }
    
    // Clear the input and refresh feedbacks
    newComment.value = ''
    await fetchFeedback()
  } catch (error) {
    console.error('Error submitting feedback:', error)
    error.value = error.message
  }
}
</script>

<template>
  <div class="single-page">
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else-if="project" class="project-review">
      <div class="top-section">
        <div class="preview-section">
          <img v-if="project.thumbnail" :src="project.thumbnail" :alt="project.title" class="preview-image">
          <div v-else class="empty-preview">No preview available</div>
        </div>
        <div class="details-section">
          <h1>{{ project.title }}</h1>
          <div class="project-meta">
            <span>By {{ project.user }}</span>
            <span>Category: {{ project.category }}</span>
          </div>
          <p class="project-description">{{ project.description }}</p>
        </div>
      </div>

      <!-- Feedback section -->
      <div class="comments-section">
        <h2>Feedback</h2>
        <div v-if="isProjectOwner" class="owner-message">
          <p>This is your project. You cannot submit feedback on your own project.</p>
        </div>
        <div v-else-if="isAuthenticated" class="comment-input">
          <textarea 
            v-model="newComment"
            placeholder="Write your feedback..."
            rows="3"
          ></textarea>
          <button @click="submitFeedback">Submit Feedback</button>
        </div>
        <div v-else class="login-message">
          Please <router-link to="/login">login</router-link> to leave feedback
        </div>

        <div class="rating-section">
          <h3>Project Rating</h3>
          <div v-if="isProjectOwner" class="owner-rating-display">
            <p class="owner-notice">This is your project</p>
            <div class="stars">
              <span v-for="i in 5" :key="i" class="star" 
                    :class="{ 'filled': i <= Math.round(project.average_rating || 0) }">★</span>
            </div>
            <div class="rating-info">
              <span v-if="project.average_rating">
                Average Rating: {{ project.average_rating.toFixed(1) }}
                <span class="rating-count">({{ project.rating_count }} ratings)</span>
              </span>
              <span v-else>No ratings yet</span>
            </div>
          </div>
          <div v-else-if="!isAuthenticated" class="login-message">
            Please <router-link to="/login">login</router-link> to rate this project
          </div>
          <div v-else>
            <StarRating 
              :project-id="project.id"
              :average-rating="project.average_rating"
              :rating-count="project.rating_count"
              @rating-updated="handleRatingUpdated"
            />
          </div>
        </div>

        <div class="comments-list">
          <div v-for="feedback in feedbacks" :key="feedback.id" class="comment">
            <div class="comment-header">
              <span class="author">{{ feedback.user }}</span>
              <span class="date">{{ new Date(feedback.created_at).toLocaleDateString() }}</span>
            </div>
            <p class="comment-content">{{ feedback.comment }}</p>
          </div>
          <div v-if="!feedbacks.length" class="no-feedback">
            No feedback yet
          </div>
        </div>
      </div>
    </div>
    <div v-else class="loading">
      Loading project...
    </div>
  </div>
</template>

<style scoped>
.single-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.project-review {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.top-section {
  display: flex;
  gap: 2rem;
}

.preview-section {
  flex: 1;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.empty-preview {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}

.details-section {
  flex: 1;
}

.project-meta {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  color: #666;
}

.project-description {
  margin: 1rem 0;
  line-height: 1.6;
}

.comments-section {
  margin-top: 2rem;
}

.comments-list {
  margin: 1rem 0;
}

.comment {
  border-bottom: 1px solid #eee;
  padding: 1rem 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.author {
  font-weight: bold;
}

.date {
  color: #666;
  font-size: 0.9rem;
}

.comment-content {
  margin: 0;
  line-height: 1.4;
}

.comment-input {
  margin-top: 1rem;
}

textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1rem;
  resize: vertical;
}

button {
  padding: 0.8rem 1.5rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background-color: #3aa876;
}

.error-message {
  color: #dc3545;
  padding: 1rem;
  margin: 1rem 0;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.login-message {
  text-align: center;
  padding: 1rem;
  color: #666;
}

.login-message a {
  color: #42b883;
  text-decoration: none;
}

.login-message a:hover {
  text-decoration: underline;
}

.rating-section {
  margin: 2rem 0;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.rating-section h3 {
  text-align: center;
  margin-bottom: 1rem;
  color: #333;
}

.owner-rating-display {
  text-align: center;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stars {
  display: flex;
  justify-content: center;
  gap: 4px;
  margin-bottom: 0.5rem;
}

.star {
  font-size: 1.5rem;
  color: #ddd;
}

.star.filled {
  color: #ffd700;
}

.rating-info {
  color: #666;
  font-size: 0.9rem;
}

.rating-count {
  color: #999;
  margin-left: 0.3rem;
}

.owner-notice {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  font-style: italic;
}

.owner-message {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
  color: #666;
  font-style: italic;
}

.no-feedback {
  text-align: center;
  padding: 1rem;
  color: #666;
  font-style: italic;
}
</style>