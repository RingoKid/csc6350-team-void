<template>
  <div class="project-card">
    <div class="project-image">
      <img :src="project.thumbnail || 'https://via.placeholder.com/300x200'" :alt="project.title" />
    </div>
    <div class="project-content">
      <div class="project-header">
        <h3>{{ project.title }}</h3>
        <span class="project-author">by {{ project.author }}</span>
      </div>
      <div class="project-category">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11a9 9 0 0 1 9 9"></path><path d="M4 4a16 16 0 0 1 16 16"></path><circle cx="5" cy="19" r="1"></circle></svg>
        {{ project.category }}
      </div>
      <div class="project-stats">
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

.project-header {
  margin-bottom: 0.5rem;
}

.project-header h3 {
  font-size: 1.3rem;
  color: #2c3e50;
}

.project-author {
  color: #666;
  font-size: 0.9rem;
}

.project-category {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.project-category svg {
  width: 16px;
  height: 16px;
}

.project-category svg path {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.project-category svg circle {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.project-category svg path:first-child {
  d: path("M4 11a9 9 0 0 1 9 9");
}

.project-category svg path:last-child {
  d: path("M4 4a16 16 0 0 1 16 16");
}

.project-category svg circle {
  cx: 5;
  cy: 19;
  r: 1;
}

.project-stats {
  margin-bottom: 1rem;
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

@media (max-width: 768px) {
  .project-actions {
    flex-direction: column;
  }
}
</style> 