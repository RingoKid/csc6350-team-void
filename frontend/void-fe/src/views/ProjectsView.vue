<template>
  <div class="projects-container">
    <h1>All Projects</h1>
    <div v-if="projects.length" class="projects-grid">
      <ProjectCard 
        v-for="project in projects" 
        :key="project.id"
        :project="project"
        :current-username="currentUsername"
        :is-superuser="isSuperuser"
      />
    </div>
    <div v-else class="no-projects">
      <p>No projects found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProjectCard from '../components/ProjectCard.vue'

const projects = ref([])
const currentUsername = ref(localStorage.getItem('username'))
const isSuperuser = ref(localStorage.getItem('is_superuser') === 'true')

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/projects/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    if (!response.ok) throw new Error('Failed to fetch projects')
    projects.value = await response.json()
  } catch (error) {
    console.error('Error fetching projects:', error)
  }
})
</script>

<style scoped>
.projects-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.no-projects {
  text-align: center;
  padding: 3rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .projects-container {
    padding: 1rem;
  }
}
</style> 