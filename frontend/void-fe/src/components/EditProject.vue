<template>
  <div class="edit-project-container">
    <div class="form-header">
      <h1>Edit Project</h1>
      <p>Update your project details</p>
    </div>

    <div v-if="loading" class="loading-message">
      Loading project details...
    </div>

    <div v-else-if="!isOwner" class="error-message">
      <i class="fas fa-exclamation-circle"></i>
      You don't have permission to edit this project.
    </div>

    <form v-else @submit.prevent="updateProject" class="edit-form">
      <div v-if="errorMessage" class="error-message">
        <i class="fas fa-exclamation-circle"></i>
        {{ errorMessage }}
      </div>

      <div v-if="successMessage" class="success-message">
        <i class="fas fa-check-circle"></i>
        {{ successMessage }}
      </div>

      <div class="form-group">
        <label for="title">Project Title</label>
        <input
          type="text"
          id="title"
          v-model="project.title"
          placeholder="Enter project title"
          required
        />
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          id="description"
          v-model="project.description"
          placeholder="Describe your project"
          rows="4"
          required
        ></textarea>
      </div>

      <div class="form-group">
        <label for="category">Category</label>
        <select id="category" v-model="project.category" required>
          <option value="">Select a category</option>
          <option v-for="category in categories" 
                  :key="category" 
                  :value="category">
            {{ category }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="thumbnail">Thumbnail URL (Optional)</label>
        <input
          type="url"
          id="thumbnail"
          v-model="project.thumbnail"
          placeholder="Enter thumbnail URL"
        />
      </div>

      <div class="form-group">
        <label for="video_url">Video URL (Optional)</label>
        <input
          type="url"
          id="video_url"
          v-model="project.video_url"
          placeholder="Enter video URL"
        />
      </div>

      <div class="form-actions">
        <button type="submit" class="submit-btn" :disabled="isSubmitting">
          {{ isSubmitting ? 'Updating...' : 'Update Project' }}
        </button>
        <router-link to="/dashboard" class="cancel-btn">Cancel</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();
    const isSubmitting = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');
    const loading = ref(true);
    const isOwner = ref(false);
    const categories = ref([
      'Hackathon',
      'Class Project',
      'Research'
    ]);
    const project = ref({
      title: '',
      description: '',
      category: '',
      thumbnail: '',
      video_url: ''
    });

    const fetchProject = async () => {
      loading.value = true;
      try {
        const response = await fetch(`http://localhost:8000/api/projects/${route.params.id}/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch project details');
        }

        const data = await response.json();
        project.value = {
          title: data.title,
          description: data.description,
          category: data.category,
          thumbnail: data.thumbnail || '',
          video_url: data.video_url || ''
        };

        // Check if current user is the owner
        const currentUsername = localStorage.getItem('username');
        isOwner.value = data.user === currentUsername;

        if (!isOwner.value) {
          router.push('/dashboard');
        }
      } catch (error) {
        console.error('Error fetching project:', error);
        errorMessage.value = 'Failed to load project details. Please try again.';
      } finally {
        loading.value = false;
      }
    };

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

    const updateProject = async () => {
      errorMessage.value = '';
      successMessage.value = '';
      if (!validateForm()) {
        return;
      }

      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return;
      }

      isSubmitting.value = true;
      try {
        const response = await fetch(`http://localhost:8000/api/projects/${route.params.id}/`, {
          method: 'PUT',
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

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.detail || 'Failed to update project');
        }

        successMessage.value = 'Project updated successfully!';
        // Wait for 1.5 seconds to show success message before redirecting
        setTimeout(() => {
          router.push('/dashboard');
        }, 1500);
      } catch (error) {
        console.error('Error updating project:', error);
        errorMessage.value = error.message || 'Failed to update project. Please try again.';
      } finally {
        isSubmitting.value = false;
      }
    };

    onMounted(() => {
      fetchProject();
    });

    return {
      project,
      categories,
      isSubmitting,
      errorMessage,
      successMessage,
      loading,
      isOwner,
      updateProject
    };
  }
};
</script>

<style scoped>
.edit-project-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.form-header p {
  color: #666;
  font-size: 1.1rem;
}

.edit-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e1e1e1;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #6a11cb;
  outline: none;
  box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.1);
}

.error-message {
  background: #fff2f2;
  color: #e74c3c;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.success-message {
  background: #edfbf6;
  color: #2ecc71;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading-message {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.submit-btn, .cancel-btn {
  flex: 1;
  padding: 0.8rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
  transition: all 0.3s ease;
}

.submit-btn {
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: white;
  border: none;
  cursor: pointer;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(106, 17, 203, 0.2);
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.cancel-btn {
  background: #f8f9fa;
  color: #666;
  border: 2px solid #e1e1e1;
  text-decoration: none;
}

.cancel-btn:hover {
  background: #e9ecef;
}

@media (max-width: 768px) {
  .edit-project-container {
    padding: 1rem;
  }

  .form-header h1 {
    font-size: 2rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style> 