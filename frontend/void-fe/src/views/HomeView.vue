<script setup>
import { ref, onMounted } from 'vue'
import StarRating from '../components/StarRating.vue'

const isLoggedIn = ref(false)
const featuredProject = ref(null)
const isLoading = ref(true)

const FEATURED_PROJECT_ID = 2 // Hardcoded featured project ID

onMounted(() => {
  checkAuthStatus()
  fetchFeaturedProject()
})

const checkAuthStatus = () => {
  const token = localStorage.getItem('access_token')
  isLoggedIn.value = !!token
}

const fetchFeaturedProject = async () => {
  try {
    const response = await fetch(`http://localhost:8000/api/projects/${FEATURED_PROJECT_ID}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    if (!response.ok) {
      throw new Error('Failed to fetch project')
    }
    const data = await response.json()
    featuredProject.value = data
  } catch (error) {
    console.error('Error fetching featured project:', error)
  } finally {
    isLoading.value = false
  }
}

const submitRating = async (rating) => {
  if (!isLoggedIn.value) {
    // Redirect to login if not logged in
    router.push('/login')
    return
  }

  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch(`http://localhost:8000/api/projects/${FEATURED_PROJECT_ID}/rate/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ rating })
    })
    
    if (!response.ok) {
      throw new Error('Failed to submit rating')
    }
    
    // Refresh project data to get updated rating
    await fetchFeaturedProject()
  } catch (error) {
    console.error('Error submitting rating:', error)
  }
}

const handleRatingUpdated = async (newRating) => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch(`http://localhost:8000/api/projects/${FEATURED_PROJECT_ID}/rate/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ rating: newRating })
    })
    
    if (!response.ok) {
      throw new Error('Failed to update rating')
    }
    
    // Refresh project data to get updated rating
    await fetchFeaturedProject()
  } catch (error) {
    console.error('Error updating rating:', error)
  }
}
</script>

<template>
  <main class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1>Showcase, Discover, and Rate Developer Projects</h1>
        <p>Welcome to SPOT! Join a community where developers share their latest creations, get constructive feedback, and find inspiration. From hackathon MVPs to polished personal projects, see what the community is building.</p>
        <div class="cta-buttons">
          <router-link to="/projects" class="primary-cta">Explore Projects</router-link>
          <router-link :to="isLoggedIn ? '/dashboard' : '/login'" class="secondary-cta">Sign Up & Share Yours</router-link>
        </div>
      </div>
    </section>

    <!-- Featured Project Section -->
    <section v-if="!isLoading" class="featured-project-section">
      <h2>Featured Project</h2>
      <div v-if="featuredProject" class="featured-project-card">
        <div class="featured-project-image">
          <img :src="featuredProject.thumbnail || 'https://picsum.photos/800/400'" :alt="featuredProject.title" />
        </div>
        <div class="featured-project-content">
          <h3>{{ featuredProject.title }}</h3>
          <p class="project-category">Category: {{ featuredProject.category }}</p>
          <p class="project-description">
            {{ featuredProject.description }}
          </p>
          <div class="project-stats">
            <StarRating
              :project-id="featuredProject.id"
              :average-rating="featuredProject.average_rating"
              :rating-count="featuredProject.rating_count"
              @rating-updated="handleRatingUpdated"
            />
          </div>
          <router-link :to="'/project/' + featuredProject.id" class="view-project-btn">View Project Details</router-link>
        </div>
      </div>
      <div v-else class="featured-project-error">
        <p>Unable to load featured project. Please try again later.</p>
      </div>
    </section>

    <!-- Loading State -->
    <section v-else class="featured-project-section loading">
      <div class="loading-spinner">Loading featured project...</div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <h2>Connect Through Code</h2>
      <div class="features-cards">
        <router-link :to="isLoggedIn ? '/dashboard' : '/login'" class="feature-card">
          <div class="icon">📤</div>
          <h3>Showcase Your Work</h3>
          <p>Easily upload details about your projects – add descriptions, tech stacks, screenshots, repository links, and live demos. Get visibility and valuable feedback from peers.</p>
        </router-link>
        <router-link to="/search" class="feature-card">
          <div class="icon">🔍</div>
          <h3>Discover New Ideas</h3>
          <p>Browse hundreds of projects across diverse categories like Web Development, AI/ML, Game Dev, Class Projects, and more. Find inspiration for your next build or learn new techniques.</p>
        </router-link>
        <router-link to="/projects" class="feature-card">
          <div class="icon">⭐</div>
          <h3>Rate and Review</h3>
          <p>Provide constructive ratings and reviews based on creativity, technical implementation, design, and utility. Help highlight outstanding work and guide fellow developers.</p>
        </router-link>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.hero-section {
  background: url('/path/to/your/background-image.jpg') no-repeat center center/cover;
  padding: 60px 20px;
  color: black;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  margin-bottom: 40px;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 20px;
}

.hero-content p {
  font-size: 1.5rem;
  margin-bottom: 30px;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.primary-cta, .secondary-cta {
  padding: 10px 20px;
  font-size: 1.2rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-decoration: none;
  display: inline-block;
}

.primary-cta {
  background-color: #6a11cb;
  color: white;
}

.secondary-cta {
  background-color: #2575fc;
  color: white;
}

.primary-cta:hover {
  background-color: #5a0fb0;
}

.secondary-cta:hover {
  background-color: #1f63d1;
}

.features-section {
  margin-top: 40px;
}

.features-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.feature-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: left;
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.icon {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #333;
}

.feature-card p {
  font-size: 1rem;
  color: #555;
  line-height: 1.6;
}

.featured-project-section {
  margin: 60px 0;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.featured-project-section h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  color: #333;
}

.featured-project-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  align-items: center;
  padding: 20px;
}

.featured-project-image img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.featured-project-content {
  text-align: left;
}

.featured-project-content h3 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #333;
}

.project-category {
  display: inline-block;
  background: #f0f0f0;
  padding: 5px 10px;
  border-radius: 4px;
  color: #666;
  margin-bottom: 15px;
}

.project-description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
  margin-bottom: 20px;
}

.project-stats {
  margin-bottom: 20px;
}

.view-project-btn {
  display: inline-block;
  padding: 12px 24px;
  background: #6a11cb;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.view-project-btn:hover {
  background: #5a0fb0;
}

@media (max-width: 768px) {
  .featured-project-card {
    grid-template-columns: 1fr;
  }
}

.loading-spinner {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.2rem;
}

.featured-project-error {
  text-align: center;
  padding: 40px;
  color: #e74c3c;
  font-size: 1.2rem;
}
</style>
