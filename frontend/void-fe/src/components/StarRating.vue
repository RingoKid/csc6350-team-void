<template>
  <div class="star-rating">
    <div v-if="!isAuthenticated" class="login-message">
      Please <router-link to="/login">login</router-link> to rate this project
    </div>
    <div v-else class="rating-container">
      <div class="stars">
        <span
          v-for="star in 5"
          :key="star"
          class="star"
          :class="{ 'active': star <= (userRating || hoverRating || 0) }"
          @mouseover="hoverRating = star"
          @mouseleave="hoverRating = 0"
          @click="rateProject(star)"
        >
          ★
        </span>
      </div>
      <div class="rating-info" v-if="averageRating">
        Average Rating: {{ averageRating.toFixed(1) }} ({{ ratingCount }} ratings)
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  },
  averageRating: {
    type: Number,
    default: 0
  },
  ratingCount: {
    type: Number,
    default: 0
  }
})

const userRating = ref(0)
const hoverRating = ref(0)
const isAuthenticated = ref(false)

onMounted(() => {
  isAuthenticated.value = !!localStorage.getItem('access_token')
  if (isAuthenticated.value) {
    fetchUserRating()
  }
})

const fetchUserRating = async () => {
  try {
    const response = await fetch(`http://localhost:8000/api/projects/${props.projectId}/ratings/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    if (!response.ok) throw new Error('Failed to fetch user rating')
    const ratings = await response.json()
    const userRatingObj = ratings.find(rating => rating.user === localStorage.getItem('username'))
    if (userRatingObj) {
      userRating.value = userRatingObj.rating
    }
  } catch (error) {
    console.error('Error fetching user rating:', error)
  }
}

const rateProject = async (rating) => {
  if (!isAuthenticated.value) return
  
  try {
    const response = await fetch(`http://localhost:8000/api/projects/${props.projectId}/rate/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({ rating })
    })
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to rate project')
    }
    userRating.value = rating
    // Emit event to update parent component
    emit('rating-updated', { rating, projectId: props.projectId })
  } catch (error) {
    console.error('Error rating project:', error)
  }
}

const emit = defineEmits(['rating-updated'])
</script>

<style scoped>
.star-rating {
  margin: 1rem 0;
}

.login-message {
  color: #666;
  font-size: 0.9rem;
}

.login-message a {
  color: #4CAF50;
  text-decoration: none;
}

.login-message a:hover {
  text-decoration: underline;
}

.rating-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.stars {
  display: flex;
  gap: 0.2rem;
}

.star {
  font-size: 1.5rem;
  color: #ddd;
  cursor: pointer;
  transition: color 0.2s;
}

.star.active {
  color: #ffd700;
}

.rating-info {
  font-size: 0.9rem;
  color: #666;
}
</style> 