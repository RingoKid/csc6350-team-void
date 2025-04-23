<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const project = ref(null)
const formData = ref({
  title: '',
  description: '',
  category: '',
  thumbnail: null
})
const error = ref(null)
const isSubmitting = ref(false)

// Configure marked options
marked.setOptions({
  breaks: true,
  gfm: true
})

// Computed property for markdown preview
const renderedPreview = computed(() => {
  if (!formData.value.description) return ''
  return marked(formData.value.description)
})

onMounted(async () => {
  try {
    const response = await fetch(`http://localhost:8000/api/projects/${route.params.id}/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to fetch project')
    }
    
    const data = await response.json()
    project.value = data
    formData.value = {
      title: data.title,
      description: data.description,
      category: data.category,
      thumbnail: null
    }
  } catch (err) {
    console.error('Error fetching project:', err)
    error.value = err.message
  }
})

const handleSubmit = async (e) => {
  e.preventDefault()
  isSubmitting.value = true
  error.value = null

  try {
    const formDataToSend = new FormData()
    formDataToSend.append('title', formData.value.title)
    formDataToSend.append('description', formData.value.description)
    formDataToSend.append('category', formData.value.category)
    if (formData.value.thumbnail) {
      formDataToSend.append('thumbnail', formData.value.thumbnail)
    }

    const response = await fetch(`http://localhost:8000/api/projects/${route.params.id}/`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: formDataToSend
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to update project')
    }

    router.push({ name: 'project', params: { id: route.params.id } })
  } catch (err) {
    console.error('Error updating project:', err)
    error.value = err.message
  } finally {
    isSubmitting.value = false
  }
}

const handleFileChange = (e) => {
  formData.value.thumbnail = e.target.files[0]
}
</script>

<template>
  <div class="edit-project">
    <h1>Edit Project</h1>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <form v-if="project" @submit="handleSubmit" class="project-form">
      <div class="form-group">
        <label for="title">Project Title</label>
        <input
          type="text"
          id="title"
          v-model="formData.title"
          required
          placeholder="Enter project title"
        >
      </div>

      <div class="form-group">
        <label for="description">Project Description</label>
        <div class="markdown-hint">
          <p>You can use Markdown to format your description. Here are some examples:</p>
          <ul>
            <li><code># Heading 1</code> for large headings</li>
            <li><code>## Heading 2</code> for smaller headings</li>
            <li><code>**bold**</code> for bold text</li>
            <li><code>*italic*</code> for italic text</li>
            <li><code>- item</code> for bullet points</li>
            <li><code>1. item</code> for numbered lists</li>
            <li><code>`code`</code> for inline code</li>
            <li><code>```code block```</code> for code blocks</li>
            <li><code>[link](url)</code> for links</li>
            <li><code>![alt](url)</code> for images</li>
          </ul>
        </div>
        <textarea
          id="description"
          v-model="formData.description"
          required
          rows="10"
          placeholder="Enter project description (supports Markdown)"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="category">Category</label>
        <select id="category" v-model="formData.category" required>
          <option value="">Select a category</option>
          <option value="web">Web Development</option>
          <option value="mobile">Mobile Development</option>
          <option value="desktop">Desktop Applications</option>
          <option value="game">Game Development</option>
          <option value="ai">Artificial Intelligence</option>
          <option value="data">Data Science</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div class="form-group">
        <label for="thumbnail">Thumbnail Image</label>
        <input
          type="file"
          id="thumbnail"
          accept="image/*"
          @change="handleFileChange"
        >
        <div v-if="project.thumbnail" class="current-thumbnail">
          <p>Current thumbnail:</p>
          <img :src="project.thumbnail" :alt="project.title" class="thumbnail-preview">
        </div>
      </div>

      <div class="preview-section">
        <h3>Preview</h3>
        <div class="markdown-preview" v-html="renderedPreview"></div>
      </div>

      <div class="form-actions">
        <button type="button" @click="router.back()" class="cancel-btn">
          Cancel
        </button>
        <button type="submit" :disabled="isSubmitting" class="submit-btn">
          {{ isSubmitting ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </form>
    <div v-else class="loading">
      Loading project...
    </div>
  </div>
</template>

<style scoped>
.edit-project {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: #1f2937;
  margin-bottom: 2rem;
  text-align: center;
}

.error-message {
  background-color: #fee2e2;
  color: #ef4444;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.project-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4b5563;
  font-weight: 500;
}

input[type="text"],
input[type="file"],
select,
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus,
input[type="file"]:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #6366f1;
}

textarea {
  resize: vertical;
  min-height: 150px;
}

.markdown-hint {
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #6b7280;
}

.markdown-hint code {
  background-color: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: monospace;
}

.current-thumbnail {
  margin-top: 1rem;
}

.current-thumbnail p {
  margin-bottom: 0.5rem;
  color: #6b7280;
}

.thumbnail-preview {
  max-width: 200px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.preview-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background-color: #f9fafb;
  border-radius: 8px;
}

.preview-section h3 {
  color: #1f2937;
  margin-bottom: 1rem;
}

.markdown-preview {
  background: white;
  padding: 1.5rem;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-btn,
.submit-btn {
  flex: 1;
  padding: 1rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: white;
  color: #6b7280;
  border: 1px solid #e5e7eb;
}

.cancel-btn:hover {
  background: #f9fafb;
}

.submit-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* Markdown preview styles */
.markdown-preview h1,
.markdown-preview h2,
.markdown-preview h3,
.markdown-preview h4,
.markdown-preview h5,
.markdown-preview h6 {
  color: #1f2937;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-preview h1 { font-size: 2em; }
.markdown-preview h2 { font-size: 1.5em; }
.markdown-preview h3 { font-size: 1.25em; }
.markdown-preview h4 { font-size: 1.1em; }
.markdown-preview h5 { font-size: 1em; }
.markdown-preview h6 { font-size: 0.9em; }

.markdown-preview p {
  margin-bottom: 1em;
  color: #4b5563;
  line-height: 1.8;
}

.markdown-preview ul,
.markdown-preview ol {
  margin-bottom: 1em;
  padding-left: 2em;
}

.markdown-preview li {
  margin-bottom: 0.5em;
  color: #4b5563;
}

.markdown-preview code {
  background-color: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: monospace;
}

.markdown-preview pre {
  background-color: #f3f4f6;
  padding: 1em;
  border-radius: 6px;
  overflow-x: auto;
  margin-bottom: 1em;
}

.markdown-preview pre code {
  background-color: transparent;
  padding: 0;
}

.markdown-preview blockquote {
  border-left: 4px solid #e5e7eb;
  padding-left: 1em;
  margin-left: 0;
  color: #6b7280;
  font-style: italic;
}

.markdown-preview a {
  color: #6366f1;
  text-decoration: none;
}

.markdown-preview a:hover {
  text-decoration: underline;
}

.markdown-preview img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  margin: 1em 0;
}

.markdown-preview table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1em;
}

.markdown-preview th,
.markdown-preview td {
  border: 1px solid #e5e7eb;
  padding: 0.5em;
  text-align: left;
}

.markdown-preview th {
  background-color: #f9fafb;
  font-weight: 600;
}
</style> 