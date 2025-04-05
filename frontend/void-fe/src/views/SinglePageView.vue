<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

interface Feedback {
  id: number
  user: number
  comment: string
  created_at: string
}

const route = useRoute()
const projectId = route.params.id

const projectTitle = ref('')
const projectDescription = ref('')
const rating = ref(0)
const newComment = ref('')
const newCommentRating = ref(5)
const projectThumbnail = ref('')

const feedbacks = ref<Feedback[]>([])

onMounted(async () => {
  try {
    const projectResponse = await fetch(`http://localhost:8000/api/projects/${projectId}/`)
    if (!projectResponse.ok) {
      throw new Error('Failed to fetch project details')
    }
    const projectData = await projectResponse.json()
    projectTitle.value = projectData.title
    projectDescription.value = projectData.description
    rating.value = projectData.rating
    projectThumbnail.value = projectData.thumbnail

    const feedbackResponse = await fetch(`http://localhost:8000/api/projects/${projectId}/feedback/`)
    if (!feedbackResponse.ok) {
      throw new Error('Failed to fetch feedback')
    }
    const feedbackData = await feedbackResponse.json()
    feedbacks.value = feedbackData
  } catch (error) {
    console.error('Error fetching project details or feedback:', error)
  }
})

const addComment = () => {
  if (newComment.value.trim()) {
    feedbacks.value.push({
      id: feedbacks.value.length + 1,
      user: 0,
      comment: newComment.value,
      created_at: new Date().toISOString().split('T')[0]
    })
    newComment.value = ''
    newCommentRating.value = 5
  }
}

</script>

<template>
    <div class="project-review">
      <div class="top-section">
        <div class="preview-section">
          <img :src="projectThumbnail" alt="Project Thumbnail" class="preview-image" v-if="projectThumbnail" />
          <div class="empty-preview" v-else>none</div>
        </div>
        <div class="details-section">
          <h1>{{ projectTitle }}</h1>
          <div class="rating">
            <span class="stars">★★★★½</span>
            <span class="rating-number">{{ rating }}/5.0</span>
          </div>
          <p class="description">{{ projectDescription }}</p>
        </div>
      </div>
  
      <!-- Feedback section -->
      <div class="comments-section">
        <h2>Feedback</h2>
        <div class="comments-list">
          <div v-for="feedback in feedbacks" :key="feedback.id" class="comment">
            <div class="comment-header">
              <span class="author">User ID: {{ feedback.user }}</span>
              <span class="date">{{ feedback.created_at }}</span>
            </div>

            <p class="comment-content">{{ feedback.comment }}</p>
          </div>
        </div>
  
        <div class="comment-input">
          <textarea 
            v-model="newComment"
            placeholder="input a comment..."
            rows="3"
          ></textarea>
          
          <!-- Select Rate -->
          <label>
            Rating:
            <select v-model="newCommentRating">
              <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
            </select>
          </label>

          <button @click="addComment">Submit</button>
        </div>
      </div>
    </div>
  </template>

<style scoped>

.comment-rating {
  margin-bottom: 0.3rem;
  color: #ffd700;
}

.empty-preview {
  min-width: 500px;
  font-size: 1.2rem;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.project-review {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.top-section {
  display: flex;
  gap: 2rem;
}

.preview-section {
  flex: 1;
  background: #f5f5f5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.details-section {
  flex: 1;
}

.comments-section {
  margin-top: 2rem;
}

.preview-image {
  max-width: 100%;
  height: auto;
}

.details-section {
  flex: 1;
}

h1 {
  margin: 0 0 1rem;
  font-size: 2rem;
}

.rating {
  margin-bottom: 1rem;
}

.stars {
  color: #ffd700;
  margin-right: 0.5rem;
}

.rating-number {
  color: #666;
}

.description {
  margin-bottom: 2rem;
  line-height: 1.6;
}

.comments-list {
  margin-bottom: 2rem;
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
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

button {
  align-self: flex-end;
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #3aa876;
}
</style>