<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Welcome to Your Dashboard</h1>
      <p>Manage and view your projects</p>
      <button class="logout-btn" @click="logout">Logout</button>
    </div>

    <div class="projects-section">
      <h2>Your Projects</h2>
      <div class="dashboard-actions">
        <router-link to="/create-project" class="create-project-btn">
          Create Project
        </router-link>
      </div>
      <div v-if="projects.length" class="projects-grid">
        <div v-for="project in projects" :key="project.id" class="project-card">
          <div class="project-image">
            <img :src="project.thumbnail || 'https://via.placeholder.com/300x200'" :alt="project.title" />
          </div>
          <div class="project-content">
            <h3>{{ project.title }}</h3>
            <p class="project-description">{{ project.description }}</p>
            <div class="project-meta">
              <span class="category">{{ project.category }}</span>
              <div class="rating-display">
                <span class="stars">
                  <span v-for="i in 5" :key="i" class="star" 
                        :class="{ 'filled': i <= Math.round(project.average_rating || 0) }">★</span>
                </span>
                <span class="rating-text" v-if="project.average_rating">
                  {{ project.average_rating.toFixed(1) }}
                  <span class="rating-count">({{ project.rating_count }})</span>
                </span>
                <span class="rating-text" v-else>No ratings yet</span>
              </div>
            </div>
            <div class="project-actions">
              <router-link :to="{ name: 'SinglePageView', params: { id: project.id }}" class="view-btn">
                View Details
              </router-link>
              <router-link :to="{ name: 'edit-project', params: { id: project.id }}" class="edit-btn">
                Edit Project
              </router-link>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-projects">
        <p>You haven't created any projects yet.</p>
        <router-link to="/create-project" class="create-btn">Create Your First Project</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const router = useRouter();
    const projects = ref([]);

    const fetchProjects = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/user/projects/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch projects');
        }
        projects.value = await response.json();
      } catch (error) {
        console.error('Error fetching projects:', error);
      }
    };

    onMounted(() => {
      fetchProjects();
    });

    const logout = () => {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user_id");
      localStorage.removeItem("username");
      window.dispatchEvent(new Event('auth-state-changed'));
      router.push("/login");
    };

    return {
      logout,
      projects
    };
  },
};
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.logout-btn {
  padding: 0.5rem 1.5rem;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #c0392b;
}

.projects-section {
  margin-top: 2rem;
}

.projects-section h2 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.project-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.project-image {
  height: 200px;
  overflow: hidden;
}

.project-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.project-content {
  padding: 1.5rem;
}

.project-content h3 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.project-description {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.category {
  background-color: #f0f0f0;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #666;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  color: #ddd;
  font-size: 1rem;
}

.star.filled {
  color: #ffd700;
}

.rating-text {
  color: #666;
  font-size: 0.9rem;
}

.rating-count {
  color: #999;
  font-size: 0.8rem;
}

.project-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.view-btn, .edit-btn {
  flex: 1;
  display: inline-block;
  padding: 0.5rem 1rem;
  text-decoration: none;
  border-radius: 4px;
  text-align: center;
  transition: all 0.3s ease;
  font-weight: 500;
}

.view-btn {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
}

.view-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.2);
}

.edit-btn {
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: white;
}

.edit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(106, 17, 203, 0.2);
}

.no-projects {
  text-align: center;
  padding: 3rem;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.no-projects p {
  color: #666;
  margin-bottom: 1rem;
}

.create-btn {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  background-color: #2ecc71;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.create-btn:hover {
  background-color: #27ae60;
}

.dashboard-actions {
  margin-bottom: 2rem;
}

.create-project-btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.create-project-btn:hover {
  background-color: #45a049;
}
</style>