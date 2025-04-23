<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import StarRating from '../components/StarRating.vue'
import ProjectFeedback from '../components/ProjectFeedback.vue'
import ReportButton from '../components/ReportButton.vue'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const project = ref(null)
const error = ref(null)
const isAuthenticated = ref(false)
const currentUsername = ref(localStorage.getItem('username'))
const isSuperuser = ref(localStorage.getItem('is_superuser') === 'true')

// Configure marked options
marked.setOptions({
  breaks: true,
  gfm: true
})

// Computed property to convert markdown to HTML
const renderedDescription = computed(() => {
  if (!project.value?.description) return ''
  return marked(project.value.description)
})

onMounted(() => {
  isAuthenticated.value = !!localStorage.getItem('access_token')
  isSuperuser.value = localStorage.getItem('is_superuser') === 'true'
  fetchProject()
})

const canEditProject = computed(() => {
  return isProjectOwner.value || isSuperuser.value
})

const isProjectOwner = computed(() => {
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
  } catch (error) {
    console.error('Error fetching project:', error)
    error.value = error.message
  }
}

const handleRatingUpdated = async () => {
  await fetchProject()
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
          <div class="project-header">
            <h1>{{ project.title }}</h1>
            <div class="project-actions">
              <router-link 
                v-if="isSuperuser || project.user === currentUsername"
                :to="{ name: 'edit-project', params: { id: project.id }}" 
                class="edit-btn"
              >
                Edit Project
              </router-link>
              <ReportButton 
                v-if="project.user !== currentUsername"
                :project-id="project.id"
                class="report-btn"
              />
            </div>
          </div>
          <div class="project-meta">
            <span>By {{ project.user }}</span>
            <span>Category: {{ project.category }}</span>
            <span v-if="isSuperuser" class="admin-badge">Admin View</span>
          </div>
          <div class="project-description markdown-content" v-html="renderedDescription"></div>
        </div>
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

      <!-- New Feedback Component -->
      <ProjectFeedback :project-id="project.id" />
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

.project-review {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.top-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
}

.preview-section {
  border-radius: 8px;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.empty-preview {
  height: 400px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}

.details-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.project-header h1 {
  font-size: 2.5rem;
  color: #1f2937;
  margin: 0;
  line-height: 1.2;
}

.project-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.edit-btn, .report-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.edit-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
}

.report-btn {
  background: white;
  color: #ef4444;
  border: 1px solid #ef4444;
}

.edit-btn:hover, .report-btn:hover {
  transform: translateY(-2px);
}

.edit-btn:hover {
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.report-btn:hover {
  background: #fee2e2;
}

.project-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #6b7280;
  font-size: 0.95rem;
}

.admin-badge {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.2));
  color: #ef4444;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.project-description {
  color: #4b5563;
  line-height: 1.8;
  font-size: 1.1rem;
}

.rating-section {
  padding: 2rem;
  border-top: 1px solid #e5e7eb;
}

.rating-section h3 {
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.owner-rating-display {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
}

.owner-notice {
  color: #6b7280;
  margin-bottom: 1rem;
}

.stars {
  display: flex;
  gap: 4px;
  margin-bottom: 0.5rem;
}

.star {
  color: #d1d5db;
  font-size: 1.5rem;
}

.star.filled {
  color: #fbbf24;
}

.rating-info {
  color: #4b5563;
}

.rating-count {
  color: #6b7280;
  font-size: 0.9rem;
}

.login-message {
  text-align: center;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  color: #6b7280;
}

.login-message a {
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
}

.login-message a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .top-section {
    grid-template-columns: 1fr;
  }

  .preview-image, .empty-preview {
    height: 300px;
  }

  .project-header {
    flex-direction: column;
  }

  .project-header h1 {
    font-size: 2rem;
  }

  .edit-btn, .report-btn {
    width: 100%;
    justify-content: center;
  }
}

.markdown-content {
  color: #4b5563;
  line-height: 1.8;
  font-size: 1.1rem;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  color: #1f2937;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-content h1 { font-size: 2em; }
.markdown-content h2 { font-size: 1.5em; }
.markdown-content h3 { font-size: 1.25em; }
.markdown-content h4 { font-size: 1.1em; }
.markdown-content h5 { font-size: 1em; }
.markdown-content h6 { font-size: 0.9em; }

.markdown-content p {
  margin-bottom: 1em;
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 1em;
  padding-left: 2em;
}

.markdown-content li {
  margin-bottom: 0.5em;
}

.markdown-content code {
  background-color: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: monospace;
}

.markdown-content pre {
  background-color: #f3f4f6;
  padding: 1em;
  border-radius: 6px;
  overflow-x: auto;
  margin-bottom: 1em;
}

.markdown-content pre code {
  background-color: transparent;
  padding: 0;
}

.markdown-content blockquote {
  border-left: 4px solid #e5e7eb;
  padding-left: 1em;
  margin-left: 0;
  color: #6b7280;
  font-style: italic;
}

.markdown-content a {
  color: #6366f1;
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}

.markdown-content img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  margin: 1em 0;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1em;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #e5e7eb;
  padding: 0.5em;
  text-align: left;
}

.markdown-content th {
  background-color: #f9fafb;
  font-weight: 600;
}
</style>