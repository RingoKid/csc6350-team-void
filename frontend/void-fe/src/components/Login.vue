<template>
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <div>
          <label for="username">Username:</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Enter your username"
            required
          />
        </div>
        <div>
          <label for="password">Password:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  
  export default {
    setup() {
      const router = useRouter();
      const username = ref("");
      const password = ref("");
      const errorMessage = ref("");
  
      const login = async () => {
        try {
          const response = await fetch("http://127.0.0.1:8000/api/token/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: username.value,
              password: password.value,
            }),
          });
  
          if (!response.ok) {
            throw new Error("Invalid username or password.");
          }
  
          const data = await response.json();
          // Save the access and refresh tokens in localStorage
          localStorage.setItem("access_token", data.access);
          localStorage.setItem("refresh_token", data.refresh);
          // Redirect to a protected page or dashboard
          router.push("/dashboard");
        } catch (error) {
          errorMessage.value = error.message || "An error occurred. Please try again.";
        }
      };
  
      return {
        username,
        password,
        errorMessage,
        login,
      };
    },
  };
  </script>
  
  <style>
  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>