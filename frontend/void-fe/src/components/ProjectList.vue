<template>
  <div class="container">
    <main>
      <!-- Hero Section -->
      <section class="carousel">
        <div class="carousel-item">
          <div class="highlighted-project">
            <h2>Highlighted Project Title</h2>
            <p>
              This is a brief description of the highlighted project. It
              showcases the main features and benefits.
            </p>
          </div>
        </div>
      </section>

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
            v-for="(project, index) in projects"
            :key="index"
          >
            <img :src="project.image" :alt="project.title" />
            <h3>{{ project.title }}</h3>
            <p>By: {{ project.author }}</p>
            <p>Rating: {{ project.rating }}</p>
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
      projects: [
        {
          image: "https://picsum.photos/300/200?random=1",
          title: "Project Title 1",
          author: "User Name 1",
          rating: "★★★★☆",
        },
        {
          image: "https://picsum.photos/300/200?random=2",
          title: "Project Title 2",
          author: "User Name 2",
          rating: "★★★★★",
        },
        {
          image: "https://picsum.photos/300/200?random=3",
          title: "Project Title 3",
          author: "User Name 3",
          rating: "★★★☆☆",
        },
        {
          image: "https://picsum.photos/300/200?random=4",
          title: "Project Title 4",
          author: "User Name 4",
          rating: "★★★★☆",
        },
        {
          image: "https://picsum.photos/300/200?random=5",
          title: "Project Title 5",
          author: "User Name 5",
          rating: "★★★★★",
        },
        {
          image: "https://picsum.photos/300/200?random=6",
          title: "Project Title 6",
          author: "User Name 6",
          rating: "★★★☆☆",
        },
        {
          image: "https://picsum.photos/300/200?random=7",
          title: "Project Title 7",
          author: "User Name 7",
          rating: "★★★★☆",
        },
        {
          image: "https://picsum.photos/300/200?random=8",
          title: "Project Title 8",
          author: "User Name 8",
          rating: "★★★★★",
        },
      ],
    };
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
.carousel {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  text-align: center;
  padding: 50px 20px;
  margin-bottom: 30px;
}

.carousel h2 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.carousel p {
  font-size: 1.2rem;
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
  background-color: #fff; /* White background for cards */
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  text-align: center;
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
</style>