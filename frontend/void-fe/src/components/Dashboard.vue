<template>
    <div class="dashboard-container">
      <h1>Welcome to the Dashboard</h1>
      <p>You have successfully logged in!</p>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  import { useRouter } from "vue-router";
  
  export default {
    setup() {
      const router = useRouter();
  
      const logout = () => {
        // Clear tokens from localStorage
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        // Redirect to the login page
        router.push("/login");
      };
  
      return {
        logout,
      };
    },
  };
  </script>
  
  <style>
  .dashboard-container {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  </style>