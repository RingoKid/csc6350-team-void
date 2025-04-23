<template>
  <div class="project-card">
    <div class="project-image">
      <img :src="project.thumbnail || 'https://via.placeholder.com/300x200'" :alt="project.title" />
    </div>
    <div class="project-content">
      <h3>{{ project.title }}</h3>
      <div class="project-author">
        <span>By {{ project.user }}</span>
        <span v-if="project.user === currentUsername" class="owner-badge">Owner</span>
      </div>
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ReportButton from './ReportButton.vue'

const props = defineProps({
  project: {
    type: Object,
    required: true
  },
  currentUsername: {
    type: String,
    required: true
  },
  isSuperuser: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
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

.view-btn, .edit-btn, .report-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.view-btn {
  background: #f3f4f6;
  color: #4b5563;
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

.view-btn:hover, .edit-btn:hover, .report-btn:hover {
  transform: translateY(-2px);
}

.edit-btn:hover {
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.report-btn:hover {
  background: #fee2e2;
}

.project-author {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.owner-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 6px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
  color: #6366f1;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

@media (max-width: 768px) {
  .project-actions {
    flex-direction: column;
  }
}
</style> 