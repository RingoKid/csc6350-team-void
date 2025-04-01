<script setup>
import Navbar from "./components/Navbar.vue";
</script>

<template>
  <div id="app">
    <!-- Header Section -->
    <header>
      <Navbar />
    </header>

    <!-- Main Content Section -->
    <main>
      <router-view />
    </main>

    <!-- Footer Section -->
    <footer>
      <p>&copy; 2025 SPOT. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
/* General Layout */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
header {
  background-color: #333;
  color: white;
  padding: 10px 20px;
}

/* Main Content */
main {
  flex: 1; /* Ensures the main content takes up available space */
  padding: 20px;
}

/* Footer */
footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 10px 0;
}
</style>