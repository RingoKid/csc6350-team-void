<template>
    <nav class="navbar">
      <div class="navbar-container">
        <a href="/" class="navbar-logo">SPOT</a>
        <ul class="navbar-links">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/project">Project</router-link></li>
          <li><router-link to="/blog">Blog</router-link></li>
          <li><router-link to="/dashboard">Dashboard</router-link></li>
          <li><router-link to="/login">Login</router-link></li>
        </ul>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: "Navbar",
  };
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
  }
  
  .navbar-links {
    list-style: none;
    display: flex;
    gap: 15px;
    margin: 0;
    padding: 0;
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
  </style>