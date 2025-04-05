<template>
  <div class="search-and-filter">
    <!-- Filters Section -->
    <aside class="filters">
      <h3>Filters</h3>
      <button class="clear-filters" @click="clearFilters">Clear All</button>

      <!-- Category Filter -->
      <div class="filter-group">
        <h4>Category</h4>
        <div v-for="category in categories" :key="category">
          <label>
            <input
              type="checkbox"
              :value="category"
              v-model="selectedCategories"
            />
            {{ category }}
          </label>
        </div>
      </div>

      <!-- Language Filter -->
      <div class="filter-group">
        <h4>Language</h4>
        <div v-for="language in languages" :key="language">
          <label>
            <input
              type="checkbox"
              :value="language"
              v-model="selectedLanguages"
            />
            {{ language }}
          </label>
        </div>
      </div>
    </aside>

    <!-- Projects Section -->
    <main class="projects">
      <div class="project-grid">
        <div
          class="project-card"
          v-for="project in filteredProjects"
          :key="project.id"
        >
          <img :src="project.image" :alt="project.title" />
          <h3>{{ project.title }}</h3>
          <p>Category: {{ project.category }}</p>
          <p>Language: {{ project.language }}</p>
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
      // Filters
      categories: ["Hackathon", "Class Project", "Research", "Other"],
      languages: ["JavaScript", "C++", "Java", "C", "Django", "C#"],
      selectedCategories: [],
      selectedLanguages: [],

      // Projects
      projects: [
        {
          id: 1,
          image: "https://picsum.photos/300/200?random=1",
          title: "Project Title 1",
          category: "Hackathon",
          language: "JavaScript",
        },
        {
          id: 2,
          image: "https://picsum.photos/300/200?random=2",
          title: "Project Title 2",
          category: "Class Project",
          language: "C++",
        },
        {
          id: 3,
          image: "https://picsum.photos/300/200?random=3",
          title: "Project Title 3",
          category: "Research",
          language: "Java",
        },
        {
          id: 4,
          image: "https://picsum.photos/300/200?random=4",
          title: "Project Title 4",
          category: "Other",
          language: "C",
        },
        {
          id: 5,
          image: "https://picsum.photos/300/200?random=5",
          title: "Project Title 5",
          category: "Hackathon",
          language: "Django",
        },
        {
          id: 6,
          image: "https://picsum.photos/300/200?random=6",
          title: "Project Title 6",
          category: "Class Project",
          language: "C#",
        },
      ],
    };
  },
  computed: {
    filteredProjects() {
      return this.projects.filter((project) => {
        const matchesCategory =
          this.selectedCategories.length === 0 ||
          this.selectedCategories.includes(project.category);
        const matchesLanguage =
          this.selectedLanguages.length === 0 ||
          this.selectedLanguages.includes(project.language);
        return matchesCategory && matchesLanguage;
      });
    },
  },
  methods: {
    clearFilters() {
      this.selectedCategories = [];
      this.selectedLanguages = [];
    },
  },
};
</script>

<style scoped>
/* Layout */
.search-and-filter {
  display: flex;
  gap: 20px;
  padding: 20px;
}

/* Filters Section */
.filters {
  width: 250px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
}

.filters h3 {
  margin-bottom: 10px;
}

.clear-filters {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}

.clear-filters:hover {
  background-color: #ff1a1a;
}

.filter-group {
  margin-bottom: 20px;
}

.filter-group h4 {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

/* Projects Section */
.projects {
  flex: 1;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.project-card {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.project-card img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: 10px;
}

.project-card h3 {
  font-size: 1.2rem;
  margin-bottom: 5px;
}

.project-card p {
  margin: 5px 0;
  color: #555;
}
</style>