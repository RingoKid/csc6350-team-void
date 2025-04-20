<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>Welcome Back</h1>
        <p class="subtitle">Sign in to continue to SPOT</p>
      </div>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <div class="input-wrapper">
            <i class="fas fa-user"></i>
            <input
              type="text"
              id="username"
              v-model="username"
              placeholder="Enter your username"
              required
            />
          </div>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="Enter your password"
              required
            />
          </div>
        </div>
        <button type="submit" class="login-button">
          Sign In
          <i class="fas fa-arrow-right"></i>
        </button>
      </form>
      <p v-if="errorMessage" class="error">
        <i class="fas fa-exclamation-circle"></i>
        {{ errorMessage }}
      </p>
      <div class="login-footer">
        <p>Don't have an account? <router-link to="/register" class="register-link">Sign up</router-link></p>
      </div>
    </div>
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
        
        // Get user ID from the token response
        const userResponse = await fetch("http://127.0.0.1:8000/api/users/", {
          headers: {
            "Authorization": `Bearer ${data.access}`
          }
        });

        if (!userResponse.ok) {
          throw new Error("Failed to get user information");
        }

        const users = await userResponse.json();
        const currentUser = users.find(user => user.username === username.value);
        if (!currentUser) {
          throw new Error("Failed to get user information");
        }

        localStorage.setItem("user_id", currentUser.id);
        localStorage.setItem("username", username.value);
        localStorage.setItem("is_superuser", currentUser.is_superuser ? 'true' : 'false');
        // Emit a custom event for login
        window.dispatchEvent(new Event('auth-state-changed'));
        // Redirect to dashboard
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

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  padding: 20px;
}

.login-container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h1 {
  color: #333;
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 700;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.login-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
  font-size: 0.95rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper i {
  position: absolute;
  left: 15px;
  color: #6a11cb;
  font-size: 1.1rem;
}

.input-wrapper input {
  width: 100%;
  padding: 12px 15px 12px 45px;
  border: 2px solid #e1e1e1;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.input-wrapper input:focus {
  border-color: #6a11cb;
  outline: none;
  box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.1);
}

.input-wrapper input::placeholder {
  color: #aaa;
}

.login-button {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(106, 17, 203, 0.2);
}

.login-button:active {
  transform: translateY(0);
}

.error {
  background: #fff2f2;
  color: #e74c3c;
  padding: 12px;
  border-radius: 8px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
}

.login-footer {
  text-align: center;
  margin-top: 30px;
  color: #666;
}

.register-link {
  color: #6a11cb;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.register-link:hover {
  color: #2575fc;
}

@media (max-width: 480px) {
  .login-container {
    padding: 30px 20px;
  }

  .login-header h1 {
    font-size: 2rem;
  }
}
</style>