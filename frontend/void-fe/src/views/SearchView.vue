<template>
  <div class="search-container">
    <div class="search-header">
      <h1>Search Projects</h1>
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search projects..."
          @input="debouncedSearch"
        />
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </div>
    </div>

    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>Searching projects...</p>
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="projects.length" class="projects-grid">
        <ProjectCard 
          v-for="project in projects" 
          :key="project.id"
          :project="project"
          :current-username="currentUsername"
          :is-superuser="isSuperuser"
        />
      </div>
      <div v-else-if="searchQuery" class="no-results">
        <p>No projects found matching "{{ searchQuery }}"</p>
      </div>
      <div v-else class="no-results">
        <p>Enter a search term to find projects</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { debounce } from 'lodash'
import ProjectCard from '../components/ProjectCard.vue'

const searchQuery = ref('')
const projects = ref([])
const isLoading = ref(false)
const error = ref(null)
const currentUsername = ref(localStorage.getItem('username'))
const isSuperuser = ref(localStorage.getItem('is_superuser') === 'true')

const searchProjects = async () => {
  if (!searchQuery.value.trim()) {
    projects.value = []
    return
  }

  try {
    isLoading.value = true
    error.value = null
    const response = await fetch(`http://localhost:8000/api/projects/search/?q=${encodeURIComponent(searchQuery.value)}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    if (!response.ok) throw new Error('Failed to search projects')
    projects.value = await response.json()
  } catch (err) {
    console.error('Error searching projects:', err)
    error.value = 'Failed to search projects. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const debouncedSearch = debounce(searchProjects, 300)

onMounted(() => {
  if (searchQuery.value) {
    searchProjects()
  }
})
</script>

<style scoped>
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.search-header {
  margin-bottom: 2rem;
}

.search-box {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.search-box input {
  width: 100%;
  padding: 1rem 1.5rem;
  padding-right: 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-box input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.search-box svg {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.loading {
  text-align: center;
  padding: 3rem;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 2rem;
  background-color: #fee2e2;
  color: #ef4444;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.no-results {
  text-align: center;
  padding: 3rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  color: #6b7280;
}

@media (max-width: 768px) {
  .search-container {
    padding: 1rem;
  }
}
</style> 