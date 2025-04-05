<script setup>
// You can add any setup logic here if needed
</script>

<template>
  <main class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1>Showcase, Discover, and Rate Developer Projects</h1>
        <p>Welcome to SPOT! Join a community where developers share their latest creations, get constructive feedback, and find inspiration. From hackathon MVPs to polished personal projects, see what the community is building.</p>
        <div class="cta-buttons">
          <button class="primary-cta">Explore Projects</button>
          <button class="secondary-cta">Sign Up & Share Yours</button>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <h2>Connect Through Code</h2>
      <div class="features-cards">
        <div class="feature-card">
          <div class="icon">📤</div>
          <h3>Showcase Your Work</h3>
          <p>Easily upload details about your projects – add descriptions, tech stacks, screenshots, repository links, and live demos. Get visibility and valuable feedback from peers.</p>
        </div>
        <div class="feature-card">
          <div class="icon">🔍</div>
          <h3>Discover New Ideas</h3>
          <p>Browse hundreds of projects across diverse categories like Web Development, AI/ML, Game Dev, Class Projects, and more. Find inspiration for your next build or learn new techniques.</p>
        </div>
        <div class="feature-card">
          <div class="icon">⭐</div>
          <h3>Rate and Review</h3>
          <p>Provide constructive ratings and reviews based on creativity, technical implementation, design, and utility. Help highlight outstanding work and guide fellow developers.</p>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.hero-section {
  background: url('/path/to/your/background-image.jpg') no-repeat center center/cover;
  padding: 60px 20px;
  color: black;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  margin-bottom: 40px;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 20px;
}

.hero-content p {
  font-size: 1.5rem;
  margin-bottom: 30px;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.primary-cta, .secondary-cta {
  padding: 10px 20px;
  font-size: 1.2rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.primary-cta {
  background-color: #6a11cb;
  color: white;
}

.secondary-cta {
  background-color: #2575fc;
  color: white;
}

.primary-cta:hover {
  background-color: #5a0fb0;
}

.secondary-cta:hover {
  background-color: #1f63d1;
}

.features-section {
  margin-top: 40px;
}

.features-cards {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.feature-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin: 10px;
  flex: 1 1 calc(33% - 20px);
  max-width: calc(33% - 20px);
  text-align: left;
}

.icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.feature-card p {
  font-size: 1rem;
  color: #555;
}
</style>
