<template>
    <nav class="navbar">
      <div class="navbar-container">
        <router-link to="/" class="navbar-logo">
          <img src="@/assets/logo.png" alt="SPOT Logo" class="logo-image" />
          <span class="logo-text">SPOT</span>
        </router-link>
        <ul class="navbar-links">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/projects">Projects</router-link></li>
          <li><router-link to="/blog">Blog</router-link></li>
          <li v-if="isLoggedIn"><router-link to="/dashboard">Dashboard</router-link></li>
          <li v-if="!isLoggedIn"><router-link to="/login">Login</router-link></li>
          <li v-else>
            <button class="logout-btn" @click="logout">Logout</button>
          </li>
        </ul>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const isLoggedIn = ref(false)

  onMounted(() => {
    isLoggedIn.value = !!localStorage.getItem('access_token')
  })

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_id')
    isLoggedIn.value = false
    router.push('/login')
  }
  </script>
  
  <style>
  .navbar {
    background-color: #333;
    color: white;
    padding: 10px 20px;
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
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .logo-image {
    height: 40px; /* Adjust this value to match your logo's desired height */
    width: auto;
    object-fit: contain;
  }

  .logo-text {
    font-size: 1.5rem;
    font-weight: bold;
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