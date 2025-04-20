<template>
    <nav class="navbar">
      <div class="navbar-container">
        <router-link to="/" class="navbar-logo">SPOT</router-link>
        <ul class="navbar-links">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/projects">Projects</router-link></li>
          <li><router-link to="/search">Search</router-link></li>
          <li><router-link to="/blog">Blog</router-link></li>
          <li v-if="isLoggedIn"><router-link to="/dashboard">Dashboard</router-link></li>
          <li v-if="!isLoggedIn"><router-link to="/login">Login</router-link></li>
          <li v-else><button @click="handleLogout" class="logout-btn">Logout</button></li>
        </ul>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const isLoggedIn = ref(false)

  const checkAuthStatus = () => {
    const token = localStorage.getItem('access_token')
    isLoggedIn.value = !!token
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('username')
    isLoggedIn.value = false
    window.dispatchEvent(new Event('auth-state-changed'))
    router.push('/login')
  }

  // Handle authentication state changes
  const handleAuthChange = () => {
    checkAuthStatus()
  }

  onMounted(() => {
    checkAuthStatus()
    // Listen for auth state changes
    window.addEventListener('auth-state-changed', handleAuthChange)
  })

  onUnmounted(() => {
    // Clean up event listener
    window.removeEventListener('auth-state-changed', handleAuthChange)
  })

  // Watch for storage events to handle login/logout in other tabs
  window.addEventListener('storage', (e) => {
    if (e.key === 'access_token') {
      checkAuthStatus()
    }
  })
  </script>
  
  <style>
  .navbar {
    background-color: #333;
    color: white;
    padding: 10px 20px;
    position: sticky;
    top: 0;
  }
  
  .navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .navbar-logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
  }
  
  .navbar-links {
    list-style: none;
    display: flex;
    gap: 15px;
    margin: 0;
    padding: 0;
    align-items: center;
  }
  
  .navbar-links li {
    display: inline;
  }
  
  .navbar-links a {
    color: white;
    text-decoration: none;
    font-size: 1rem;
  }
  
  .navbar-links a:hover {
    text-decoration: underline;
  }

  .logout-btn {
    background-color: #e74c3c;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s;
  }

  .logout-btn:hover {
    background-color: #c0392b;
  }
  </style>