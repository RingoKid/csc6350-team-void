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
        <h1 class="hero-title">
          <span class="gradient-text">Showcase</span>, 
          <span class="gradient-text">Discover</span>, and 
          <span class="gradient-text">Rate</span>
          <div class="subtitle">Developer Projects</div>
        </h1>
        <p class="hero-description">Welcome to SPOT! Join a community where developers share their latest creations, get constructive feedback, and find inspiration. From hackathon MVPs to polished personal projects, see what the community is building.</p>
        <div class="cta-buttons">
          <router-link to="/projects" class="primary-cta">
            <span>Explore Projects</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
          </router-link>
          <router-link :to="isLoggedIn ? '/dashboard' : '/login'" class="secondary-cta">
            <span>Sign Up & Share Yours</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path><polyline points="10 17 15 12 10 7"></polyline><line x1="15" y1="12" x2="3" y2="12"></line></svg>
          </router-link>
        </div>
      </div>
      <div class="hero-background">
        <div class="gradient-circle circle-1"></div>
        <div class="gradient-circle circle-2"></div>
        <div class="gradient-circle circle-3"></div>
      </div>
    </section>

    <!-- Featured Project Section -->
    <section v-if="!isLoading" class="featured-project-section">
      <h2 class="section-title">
        <span class="gradient-text">Featured</span> Project
      </h2>
      <div v-if="featuredProject" class="featured-project-card">
        <div class="featured-project-image">
          <img :src="featuredProject.thumbnail || 'https://picsum.photos/800/400'" :alt="featuredProject.title" />
          <div class="image-overlay"></div>
        </div>
        <div class="featured-project-content">
          <div class="project-header">
            <h3>{{ featuredProject.title }}</h3>
            <span class="project-category">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11a9 9 0 0 1 9 9"></path><path d="M4 4a16 16 0 0 1 16 16"></path><circle cx="5" cy="19" r="1"></circle></svg>
              {{ featuredProject.category }}
            </span>
          </div>
          <p class="project-description">
            {{ featuredProject.description }}
          </p>
          <div class="project-stats">
            <div class="rating-display">
              <span class="stars">
                <span v-for="i in 5" 
                      :key="i" 
                      class="star"
                      :class="{ 'filled': i <= Math.round(featuredProject.average_rating || 0) }">★</span>
              </span>
              <span class="rating-text">
                {{ featuredProject.average_rating?.toFixed(1) || '0.0' }}
                <span class="rating-count">({{ featuredProject.rating_count || 0 }} ratings)</span>
              </span>
            </div>
          </div>
          <router-link :to="'/project/' + featuredProject.id" class="view-project-btn">
            <span>View Project Details</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
          </router-link>
        </div>
      </div>
      <div v-else class="featured-project-error">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        <p>Unable to load featured project. Please try again later.</p>
      </div>
    </section>

    <!-- Loading State -->
    <section v-else class="featured-project-section loading">
      <div class="loading-spinner">
        <svg class="spinner" viewBox="0 0 50 50">
          <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
        </svg>
        Loading featured project...
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <h2 class="section-title">
        Connect <span class="gradient-text">Through Code</span>
      </h2>
      <div class="features-cards">
        <router-link :to="isLoggedIn ? '/dashboard' : '/login'" class="feature-card">
          <div class="icon-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
          </div>
          <h3>Showcase Your Work</h3>
          <p>Easily upload details about your projects – add descriptions, tech stacks, screenshots, repository links, and live demos. Get visibility and valuable feedback from peers.</p>
          <div class="card-arrow">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </div>
        </router-link>
        <router-link to="/search" class="feature-card">
          <div class="icon-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </div>
          <h3>Discover New Ideas</h3>
          <p>Browse hundreds of projects across diverse categories like Web Development, AI/ML, Game Dev, Class Projects, and more. Find inspiration for your next build or learn new techniques.</p>
          <div class="card-arrow">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </div>
        </router-link>
        <router-link to="/projects" class="feature-card">
          <div class="icon-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
          </div>
          <h3>Rate and Review</h3>
          <p>Provide constructive ratings and reviews based on creativity, technical implementation, design, and utility. Help highlight outstanding work and guide fellow developers.</p>
          <div class="card-arrow">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </div>
        </router-link>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.hero-section {
  position: relative;
  padding: 100px 20px;
  margin-bottom: 60px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 30px;
  color: #2c3e50;
}

.gradient-text {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 3.5rem;
  margin-top: 10px;
  color: #2c3e50;
}

.hero-description {
  font-size: 1.25rem;
  line-height: 1.8;
  color: #4a5568;
  margin-bottom: 40px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: center;
}

.primary-cta, .secondary-cta {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
  text-decoration: none;
}

.primary-cta {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
}

.primary-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.secondary-cta {
  background: white;
  color: #6366f1;
  border: 2px solid #6366f1;
}

.secondary-cta:hover {
  background: rgba(99, 102, 241, 0.1);
  transform: translateY(-2px);
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  overflow: hidden;
}

.gradient-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
}

.circle-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  top: -100px;
  right: -100px;
}

.circle-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  bottom: -50px;
  left: -50px;
}

.circle-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #34d399, #10b981);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 2rem;
  }
  
  .hero-description {
    font-size: 1.1rem;
    padding: 0 20px;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
  
  .primary-cta, .secondary-cta {
    width: 100%;
    justify-content: center;
  }
}

.features-section {
  margin: 80px 0;
  padding: 40px 20px;
  position: relative;
}

.features-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.feature-card {
  position: relative;
  background: white;
  border-radius: 20px;
  padding: 30px;
  text-align: left;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.feature-card:hover::before {
  opacity: 1;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 16px;
  margin-bottom: 24px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
  color: #6366f1;
  transition: all 0.3s ease;
}

.feature-card:hover .icon-wrapper {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  transform: scale(1.1);
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #2c3e50;
}

.feature-card p {
  font-size: 1rem;
  line-height: 1.7;
  color: #4a5568;
  margin-bottom: 24px;
}

.card-arrow {
  position: absolute;
  bottom: 20px;
  right: 20px;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
  color: #6366f1;
}

.feature-card:hover .card-arrow {
  opacity: 1;
  transform: translateX(0);
}

.featured-project-section {
  margin: 80px 0;
  padding: 40px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.section-title {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.featured-project-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
  padding: 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.featured-project-image {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transition: transform 0.3s ease;
}

.featured-project-image:hover {
  transform: translateY(-5px);
}

.featured-project-image img {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.3s ease;
}

.featured-project-image:hover img {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.2) 100%);
  pointer-events: none;
}

.project-header {
  margin-bottom: 24px;
}

.project-header h3 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 12px;
  line-height: 1.2;
}

.project-category {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
  padding: 8px 16px;
  border-radius: 20px;
  color: #6366f1;
  font-weight: 500;
  font-size: 0.95rem;
}

.project-category svg {
  opacity: 0.8;
}

.project-description {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #4a5568;
  margin-bottom: 24px;
}

.project-stats {
  margin-bottom: 24px;
  padding: 16px 0;
  border-top: 1px solid rgba(0,0,0,0.1);
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  color: #ddd;
  font-size: 1.2rem;
}

.star.filled {
  color: #ffd700;
}

.rating-text {
  color: #666;
  font-size: 0.95rem;
}

.rating-count {
  color: #999;
  font-size: 0.85rem;
  margin-left: 0.3rem;
}

.view-project-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.view-project-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.view-project-btn svg {
  transition: transform 0.3s ease;
}

.view-project-btn:hover svg {
  transform: translateX(4px);
}

.featured-project-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px;
  color: #e53e3e;
  font-size: 1.2rem;
  background: rgba(229, 62, 62, 0.1);
  border-radius: 12px;
}

.featured-project-error svg {
  color: #e53e3e;
  width: 32px;
  height: 32px;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px;
  color: #6366f1;
  font-size: 1.2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  animation: rotate 2s linear infinite;
}

.spinner .path {
  stroke: #6366f1;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}

@media (max-width: 768px) {
  .featured-project-section {
    padding: 30px 20px;
    margin: 40px 0;
  }

  .section-title {
    font-size: 2rem;
  }

  .featured-project-card {
    grid-template-columns: 1fr;
    gap: 30px;
    padding: 15px;
  }

  .project-header h3 {
    font-size: 1.8rem;
  }

  .project-description {
    font-size: 1rem;
  }
}
</style>
