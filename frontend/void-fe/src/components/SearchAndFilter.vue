<template>
  <div class="search-and-filter">
    <!-- Filters Section -->
    <aside class="filters">
      <h3>Filters</h3>
      <button class="clear-filters" @click="clearFilters">Clear All</button>

      <!-- Category Filter -->
      <div class="filter-group">
        <h4>Category</h4>
        <div v-for="category in uniqueCategories" :key="category">
          <label class="filter-label">
            <input
              type="checkbox"
              :value="category"
              v-model="selectedCategories"
            />
            {{ category }}
          </label>
        </div>
      </div>

      <!-- Search by Title -->
      <div class="filter-group">
        <h4>Search by Title</h4>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search by title..."
          class="search-input"
        />
      </div>

      <!-- Search by User -->
      <div class="filter-group">
        <h4>Search by User</h4>
        <input
          type="text"
          v-model="userSearchQuery"
          placeholder="Search by username..."
          class="search-input"
        />
        <div v-if="userSearchQuery && filteredUsers.length > 0" class="user-suggestions">
          <div 
            v-for="user in filteredUsers" 
            :key="user"
            class="user-suggestion"
            @click="selectUser(user)"
            :class="{ 'selected': selectedUsers.includes(user) }"
          >
            <span>{{ user }}</span>
            <span v-if="selectedUsers.includes(user)" class="check-mark">✓</span>
          </div>
        </div>
        <div v-if="selectedUsers.length > 0" class="selected-users">
          <div v-for="user in selectedUsers" :key="user" class="selected-user">
            {{ user }}
            <button @click="removeUser(user)" class="remove-user">×</button>
          </div>
        </div>
      </div>
    </aside>

    <!-- Projects Section -->
    <main class="projects">
      <div v-if="isLoading" class="loading-state">
        <p>Loading projects...</p>
      </div>
      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
      </div>
      <div v-else>
        <h2>Found {{ filteredProjects.length }} Projects</h2>
        <div class="project-grid">
          <div
            class="project-card"
            v-for="project in filteredProjects"
            :key="project.id"
          >
            <router-link :to="`/project/${project.id}`" class="project-link">
              <img 
                :src="project.thumbnail || 'https://picsum.photos/300/200'" 
                :alt="project.title" 
              />
              <div class="project-content">
                <h3>{{ project.title }}</h3>
                <p class="author">By: {{ project.user }}</p>
                <p class="category">{{ project.category }}</p>
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
            </router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "SearchAndFilter",
  data() {
    return {
      projects: [],
      selectedCategories: [],
      searchQuery: "",
      userSearchQuery: "",
      selectedUsers: [],
      isLoading: true,
      error: null
    };
  },
  computed: {
    uniqueCategories() {
      return [...new Set(this.projects.map(project => project.category))].sort();
    },
    uniqueUsers() {
      return [...new Set(this.projects.map(project => project.user))];
    },
    filteredUsers() {
      if (!this.userSearchQuery) return [];
      const query = this.userSearchQuery.toLowerCase();
      return this.uniqueUsers
        .filter(user => 
          user.toLowerCase().includes(query) && 
          !this.selectedUsers.includes(user)
        )
        .slice(0, 5); // Limit to 5 suggestions
    },
    filteredProjects() {
      return this.projects.filter((project) => {
        const matchesCategory =
          this.selectedCategories.length === 0 ||
          this.selectedCategories.includes(project.category);
        
        const matchesSearch =
          !this.searchQuery ||
          project.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          project.description.toLowerCase().includes(this.searchQuery.toLowerCase());

        const matchesUser =
          this.selectedUsers.length === 0 ||
          this.selectedUsers.includes(project.user);

        return matchesCategory && matchesSearch && matchesUser;
      });
    },
  },
  methods: {
    clearFilters() {
      this.selectedCategories = [];
      this.searchQuery = "";
      this.userSearchQuery = "";
      this.selectedUsers = [];
    },
    selectUser(user) {
      if (!this.selectedUsers.includes(user)) {
        this.selectedUsers.push(user);
      }
      this.userSearchQuery = ""; // Clear the search after selection
    },
    removeUser(user) {
      this.selectedUsers = this.selectedUsers.filter(u => u !== user);
    },
    async fetchProjects() {
      try {
        const response = await fetch('http://localhost:8000/api/projects/');
        if (!response.ok) {
          throw new Error('Failed to fetch projects');
        }
        this.projects = await response.json();
      } catch (error) {
        this.error = 'Error loading projects. Please try again later.';
        console.error('Error fetching projects:', error);
      } finally {
        this.isLoading = false;
      }
    }
  },
  async created() {
    await this.fetchProjects();
  }
};
</script>

<style scoped>
.search-and-filter {
  display: flex;
  gap: 30px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Filters Section */
.filters {
  width: 280px;
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.filters h3 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.clear-filters {
  background: linear-gradient(135deg, #ff4d4d 0%, #ff1a1a 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 25px;
  font-weight: 500;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.clear-filters:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 26, 26, 0.2);
}

.filter-group {
  margin-bottom: 25px;
  position: relative;
}

.filter-group h4 {
  color: #444;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  color: #555;
  transition: color 0.2s ease;
}

.filter-label:hover {
  color: #6a11cb;
}

.search-input {
  width: 100%;
  padding: 10px 15px;
  border: 2px solid #e1e1e1;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #6a11cb;
  outline: none;
  box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.1);
}

/* Projects Section */
.projects {
  flex: 1;
}

.projects h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 1.8rem;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.project-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.project-link {
  text-decoration: none;
  color: inherit;
}

.project-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.project-content {
  padding: 20px;
}

.project-card h3 {
  font-size: 1.3rem;
  margin-bottom: 10px;
  color: #333;
}

.author {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.category {
  display: inline-block;
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 12px;
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

.loading-state, .error-state {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.loading-state {
  color: #666;
}

.error-state {
  color: #e74c3c;
}

.user-suggestions {
  position: absolute;
  width: 100%;
  background: white;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  margin-top: 5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.user-suggestion {
  padding: 8px 15px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s ease;
}

.user-suggestion:hover {
  background-color: #f5f5f5;
  color: #6a11cb;
}

.user-suggestion.selected {
  background-color: #f0f0f0;
  color: #6a11cb;
}

.check-mark {
  color: #6a11cb;
  font-weight: bold;
}

.selected-users {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.selected-user {
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.85rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 8px;
}

.remove-user {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 0;
  font-size: 1.2rem;
  line-height: 1;
  transition: color 0.2s ease;
}

.remove-user:hover {
  color: #ff4d4d;
}

@media (max-width: 768px) {
  .search-and-filter {
    flex-direction: column;
  }

  .filters {
    width: 100%;
  }
}
</style>