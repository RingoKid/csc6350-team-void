<template>
  <div class="container">
    <main>
      <!-- Hero Section -->
      <section class="featured-hero" v-if="!isLoading">
        <div v-if="featuredProject" class="featured-content">
          <div class="featured-image">
            <img :src="featuredProject.thumbnail || 'https://picsum.photos/800/400'" :alt="featuredProject.title" />
          </div>
          <div class="featured-details">
            <h2>Featured Project</h2>
            <h3>{{ featuredProject.title }}</h3>
            <p class="featured-category">Category: {{ featuredProject.category }}</p>
            <p class="featured-description">{{ featuredProject.description }}</p>
            <div class="featured-stats">
              <div class="rating-display">
                <span class="stars">
                  <span v-for="i in 5" :key="i" class="star" 
                        :class="{ 'filled': i <= Math.round(featuredProject.average_rating || 0) }">★</span>
                </span>
                <span class="rating-text" v-if="featuredProject.average_rating">
                  {{ featuredProject.average_rating.toFixed(1) }}
                  <span class="rating-count">({{ featuredProject.rating_count }})</span>
                </span>
                <span class="rating-text" v-else>No ratings yet</span>
              </div>
            </div>
            <router-link :to="'/project/' + featuredProject.id" class="view-featured-btn">
              View Project Details
            </router-link>
          </div>
        </div>
        <div v-else class="featured-error">
          <p>Unable to load featured project. Please try again later.</p>
        </div>
      </section>
      <div v-else class="featured-loading">
        <p>Loading featured project...</p>
      </div>

      <!-- Fun Feature Section -->
      <section class="fun-feature">
        <div class="fun-feature-block">
          <p>🎉 Fun Feature: Discover amazing projects and connect with creators! 🎉</p>
        </div>
      </section>

      <!-- Project Cards Section -->
      <section class="project-grid-wrapper">
        <h2>Explore Projects</h2>
        <div class="project-cards">
          <div
            class="project-card"
            v-for="project in projects"
            :key="project.id"
          >
            <router-link :to="`/project/${project.id}`" class="project-link">
              <img :src="project.thumbnail || 'https://via.placeholder.com/300x200'" :alt="project.title" />
              <h3>{{ project.title }}</h3>
              <div class="project-info">
                <p class="author">By: {{ project.user }}</p>
                <p class="category">{{ project.category }}</p>
                <div class="rating-display">
                  <span class="stars" v-if="project.average_rating">
                    <span v-for="i in 5" :key="i" class="star" 
                          :class="{ 'filled': i <= Math.round(project.average_rating) }">★</span>
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
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "ProjectList",
  data() {
    return {
      projects: [],
      featuredProject: null,
      isLoading: true,
      FEATURED_PROJECT_ID: 2, // Same as home page
    };
  },
  async created() {
    await Promise.all([
      this.fetchProjects(),
      this.fetchFeaturedProject()
    ]);
  },
  methods: {
    async fetchProjects() {
      try {
        const response = await fetch('http://localhost:8000/api/projects/');
        if (!response.ok) {
          throw new Error('Failed to fetch projects');
        }
        this.projects = await response.json();
      } catch (error) {
        console.error('Error fetching projects:', error);
      }
    },
    async fetchFeaturedProject() {
      try {
        const response = await fetch(`http://localhost:8000/api/projects/${this.FEATURED_PROJECT_ID}/`);
        if (!response.ok) {
          throw new Error('Failed to fetch featured project');
        }
        this.featuredProject = await response.json();
      } catch (error) {
        console.error('Error fetching featured project:', error);
      } finally {
        this.isLoading = false;
      }
    }
  },
};
</script>

<style scoped>
/* General Layout */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

/* Container */
.container {
  max-width: 1200px; /* Limit the width of the container */
  margin: 0 auto; /* Center the container horizontally */
  padding: 0 20px; /* Add padding for smaller screens */
}

/* Hero Section */
.featured-hero {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
  overflow: hidden;
}

.featured-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  padding: 30px;
}

.featured-image img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.featured-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.featured-details h2 {
  color: #6a11cb;
  font-size: 1.5rem;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.featured-details h3 {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: #333;
}

.featured-category {
  display: inline-block;
  background: #f0f0f0;
  padding: 5px 15px;
  border-radius: 20px;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 20px;
}

.featured-description {
  color: #555;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 25px;
}

.featured-stats {
  margin-bottom: 25px;
}

.view-featured-btn {
  display: inline-block;
  padding: 12px 24px;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  text-align: center;
  max-width: 200px;
}

.view-featured-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(106, 17, 203, 0.2);
}

.featured-loading, .featured-error {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 12px;
  margin-bottom: 30px;
}

.featured-loading {
  color: #666;
}

.featured-error {
  color: #e74c3c;
}

@media (max-width: 768px) {
  .featured-content {
    grid-template-columns: 1fr;
  }

  .featured-image img {
    height: 300px;
  }

  .featured-details h3 {
    font-size: 2rem;
  }
}

/* Fun Feature Section */
.fun-feature {
  background-color: #f9f9f9;
  padding: 20px;
  text-align: center;
  margin-bottom: 30px;
}

.fun-feature p {
  font-size: 1.2rem;
  color: #333;
}

/* Project Cards Section Wrapper */
.project-grid-wrapper {
  background-color: #f9f9f9; /* Light background for distinction */
  border: 1px solid #ddd; /* Add a border to frame the section */
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

.project-grid-wrapper h2 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

/* Project Cards Section */
.project-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  justify-content: center;
}

.project-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.project-link {
  text-decoration: none;
  color: inherit;
  flex: 1;
}

.rating-wrapper {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

/* Remove the hover color change for rating text */
.project-card:hover .rating-wrapper {
  color: inherit;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.project-card img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc; /* Add a border around the image */
}

.project-card h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #333;
}

.project-card p {
  margin: 5px 0;
  color: #555;
}

/* Add subtle hover effect for the card text */
.project-card:hover h3 {
  color: #6a11cb; /* Highlight the title on hover */
}

.project-card:hover p {
  color: #2575fc; /* Highlight the text on hover */
}

.project-info {
  padding: 0.5rem;
  text-align: left;
}

.project-info p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.author {
  font-weight: 500;
  color: #2c3e50 !important;
}

.category {
  background-color: #f0f0f0;
  display: inline-block;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem !important;
}

.rating-display {
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
  margin-left: 0.2rem;
}

.project-card a {
  text-decoration: none;
  color: inherit;
}
</style>