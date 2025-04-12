<template>
  <div class="edit-project-container">
    <h1>Edit Project</h1>
    <form @submit.prevent="updateProject" class="edit-project-form">
      <div class="form-group">
        <label for="title">Title</label>
        <input
          type="text"
          id="title"
          v-model="formData.title"
          required
        />
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          id="description"
          v-model="formData.description"
          required
        ></textarea>
      </div>

      <div class="form-group">
        <label for="category">Category</label>
        <select id="category" v-model="formData.category" required>
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
          v-model="formData.thumbnail"
          placeholder="https://example.com/image.jpg"
        />
      </div>

      <div class="error-message" v-if="error">{{ error }}</div>

      <div class="form-actions">
        <button type="submit" class="update-btn">Update Project</button>
        <button type="button" class="cancel-btn" @click="cancelEdit">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const projectId = route.params.id
const error = ref('')

const formData = ref({
  title: '',
  description: '',
  category: '',
  thumbnail: '',
  user: ''
})

onMounted(async () => {
  try {
    const response = await fetch(`http://localhost:8000/api/projects/${projectId}/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/login')
        return
      }
      throw new Error('Failed to fetch project details')
    }

    const project = await response.json()
    formData.value = {
      title: project.title,
      description: project.description,
      category: project.category,
      thumbnail: project.thumbnail || '',
      user: project.user
    }
  } catch (err) {
    error.value = err.message
  }
})

const updateProject = async () => {
  try {
    // Create a clean request body with only the fields that have values
    const requestBody = {
      title: formData.value.title,
      description: formData.value.description,
      category: formData.value.category,
      user: formData.value.user
    }

    // Only include thumbnail if it has a value
    if (formData.value.thumbnail) {
      requestBody.thumbnail = formData.value.thumbnail
    }

    const response = await fetch(`http://localhost:8000/api/projects/${projectId}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(requestBody)
    })

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/login')
        return
      }
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to update project')
    }

    router.push('/dashboard')
  } catch (err) {
    error.value = err.message
  }
}

const cancelEdit = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
.edit-project-container {
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

.edit-project-form {
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
  font-weight: 500;
  color: #2c3e50;
}

input,
textarea,
select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

textarea {
  min-height: 150px;
  resize: vertical;
}

.error-message {
  color: #e74c3c;
  text-align: center;
  margin: 1rem 0;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.update-btn,
.cancel-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.update-btn {
  background-color: #f39c12;
  color: white;
}

.update-btn:hover {
  background-color: #e67e22;
}

.cancel-btn {
  background-color: #95a5a6;
  color: white;
}

.cancel-btn:hover {
  background-color: #7f8c8d;
}
</style> 