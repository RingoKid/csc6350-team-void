<template>
  <div class="signup-container">
    <div class="signup-card">
      <h2>Create an Account</h2>
      <form @submit.prevent="handleSubmit" class="signup-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            placeholder="Enter your username"
          />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            placeholder="Enter your email"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            placeholder="Enter your password"
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            required
            placeholder="Confirm your password"
          />
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        <button type="submit" class="signup-button" :disabled="loading">
          {{ loading ? 'Creating Account...' : 'Sign Up' }}
        </button>
        <div class="login-link">
          Already have an account? <router-link to="/login">Login</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'SignUp',
  setup() {
    const router = useRouter();
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const errorMessage = ref('');
    const loading = ref(false);

    const handleSubmit = async () => {
      if (password.value !== confirmPassword.value) {
        errorMessage.value = 'Passwords do not match';
        return;
      }

      loading.value = true;
      errorMessage.value = '';

      try {
        const response = await fetch('http://127.0.0.1:8000/api/auth/signup/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username.value,
            email: email.value,
            password: password.value,
            confirm_password: password.value,
            role: 'Presenter'  // Default role
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || Object.values(data)[0][0] || 'Registration failed');
        }

        // Automatically log in the user after successful registration
        const loginResponse = await fetch('http://127.0.0.1:8000/api/token/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username.value,
            password: password.value,
          }),
        });

        const loginData = await loginResponse.json();

        if (!loginResponse.ok) {
          throw new Error('Login failed after registration');
        }

        localStorage.setItem('access_token', loginData.access);
        localStorage.setItem('refresh_token', loginData.refresh);
        localStorage.setItem('username', username.value);

        // Emit auth state change event
        window.dispatchEvent(new Event('auth-state-changed'));
        
        router.push('/');
      } catch (error) {
        errorMessage.value = error.message;
      } finally {
        loading.value = false;
      }
    };

    return {
      username,
      email,
      password,
      confirmPassword,
      errorMessage,
      loading,
      handleSubmit,
    };
  },
};
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  padding: 1rem;
}

.signup-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #2575fc;
}

.error-message {
  color: #dc3545;
  font-size: 0.9rem;
  text-align: center;
}

.signup-button {
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.signup-button:hover {
  opacity: 0.9;
}

.signup-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}

.login-link a {
  color: #2575fc;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}
</style> 