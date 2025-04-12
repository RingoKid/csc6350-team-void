<template>
  <div class="create-project-container">
    <h1>Create New Project</h1>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    <form @submit.prevent="createProject" class="project-form">
      <div class="form-group">
        <label for="title">Project Title</label>
        <input 
          type="text" 
          id="title" 
          v-model="project.title" 
          required 
          placeholder="Enter project title"
        />
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea 
          id="description" 
          v-model="project.description" 
          required 
          placeholder="Describe your project"
          rows="4"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="category">Category</label>
        <select id="category" v-model="project.category" required>
          <option value="">Select a category</option>
          <option value="Hackathon">Hackathon</option>
          <option value="Class Project">Class Project</option>
          <option value="Research">Research</option>
        </select>
      </div>

      <div class="form-group">
        <label for="thumbnail">Thumbnail URL</label>
        <input 
          type="url" 
          id="thumbnail" 
          v-model="project.thumbnail" 
          placeholder="Enter image URL for your project"
        />
      </div>

      <div class="form-group">
        <label for="video_url">Video URL (optional)</label>
        <input 
          type="url" 
          id="video_url" 
          v-model="project.video_url" 
          placeholder="Enter video URL for your project"
        />
      </div>

      <div class="form-actions">
        <button type="submit" class="submit-btn" :disabled="isSubmitting">
          {{ isSubmitting ? 'Creating...' : 'Create Project' }}
        </button>
        <router-link to="/dashboard" class="cancel-btn">Cancel</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const isSubmitting = ref(false);
    const errorMessage = ref('');
    const userId = ref(null);
    const project = ref({
      title: '',
      description: '',
      category: '',
      thumbnail: '',
      video_url: ''
    });

    onMounted(() => {
      const token = localStorage.getItem('access_token');
      const storedUserId = localStorage.getItem('user_id');
      if (!token || !storedUserId) {
        router.push('/login');
        return;
      }
      userId.value = storedUserId;
    });

    const validateForm = () => {
      if (!project.value.title.trim()) {
        errorMessage.value = 'Project title is required';
        return false;
      }
      if (!project.value.description.trim()) {
        errorMessage.value = 'Project description is required';
        return false;
      }
      if (!project.value.category) {
        errorMessage.value = 'Please select a category';
        return false;
      }
      return true;
    };

    const createProject = async () => {
      errorMessage.value = '';
      if (!validateForm()) {
        return;
      }

      const token = localStorage.getItem('access_token');
      if (!token || !userId.value) {
        router.push('/login');
        return;
      }

      isSubmitting.value = true;
      try {
        const response = await fetch('http://localhost:8000/api/projects/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            title: project.value.title.trim(),
            description: project.value.description.trim(),
            category: project.value.category,
            thumbnail: project.value.thumbnail.trim() || null,
            video_url: project.value.video_url.trim() || null
          })
        });

        if (response.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user_id');
          router.push('/login');
          return;
        }

        const data = await response.json();
        
        if (!response.ok) {
          if (typeof data === 'object' && data !== null) {
            const errors = Object.entries(data)
              .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages[0] : messages}`)
              .join('\n');
            throw new Error(errors || 'Failed to create project');
          }
          throw new Error(data.detail || 'Failed to create project');
        }

        router.push('/dashboard');
      } catch (error) {
        console.error('Error creating project:', error);
        errorMessage.value = error.message || 'Failed to create project. Please try again.';
      } finally {
        isSubmitting.value = false;
      }
    };

    return {
      project,
      isSubmitting,
      errorMessage,
      createProject
    };
  }
};
</script>

<style scoped>
.create-project-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.project-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  color: #2c3e50;
}

input, textarea, select {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

textarea {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.submit-btn {
  flex: 1;
  padding: 0.8rem 1.5rem;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #27ae60;
}

.submit-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.cancel-btn {
  padding: 0.8rem 1.5rem;
  background-color: #e74c3c;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.cancel-btn:hover {
  background-color: #c0392b;
}

.error-message {
  background-color: #fee2e2;
  border: 1px solid #ef4444;
  color: #b91c1c;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  white-space: pre-line;
}
</style> 