<script setup lang="ts">
import { ref } from 'vue'

interface Comment {
  id: number
  author: string
  content: string
  date: string
  rating: number
}

const projectTitle = ref('Project')
const projectDescription = ref('Description of the project')
const rating = ref(4.5)
const newComment = ref('')
const newCommentRating = ref(5)

const comments = ref<Comment[]>([
  {
    id: 1,
    author: 'John Doe',
    content: 'Good!',
    date: '2024-03-15',
    rating: 4
  },
  {
    id: 2,
    author: 'Mary Jane',
    content: 'Nice.',
    date: '2024-03-14',
    rating: 4.5
  }
])

const addComment = () => {
  if (newComment.value.trim()) {
    comments.value.push({
      id: comments.value.length + 1,
      author: 'User',
      content: newComment.value,
      date: new Date().toISOString().split('T')[0],
      rating: newCommentRating.value
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
          <div class="empty-preview">none</div>
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
  
      <!-- ✅ comment section moved outside and below -->
      <div class="comments-section">
                <h2>Comment</h2>
                <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment">
            <div class="comment-header">
            <span class="author">{{ comment.author }}</span>
            <span class="date">{{ comment.date }}</span>
            </div>

            <!-- Comment Rate -->
            <div class="comment-rating">
            <span class="stars">
                {{ '★'.repeat(comment.rating) + '☆'.repeat(5 - comment.rating) }}
            </span>
            </div>

            <p class="comment-content">{{ comment.content }}</p>
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