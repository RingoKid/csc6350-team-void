<template>
  <div class="nav-container">
    <nav class="navbar">
      <router-link to="/" class="nav-brand">
        <h1>SPOT</h1>
      </router-link>

      <div class="nav-links">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
          Home
        </router-link>
        <router-link to="/projects" class="nav-link" :class="{ active: $route.path === '/projects' }">
          Projects
        </router-link>
        <router-link to="/search" class="nav-link" :class="{ active: $route.path === '/search' }">
          Search
        </router-link>
        <router-link v-if="isLoggedIn" to="/dashboard" class="nav-link" :class="{ active: $route.path === '/dashboard' }">
          Dashboard
        </router-link>
      </div>

      <div class="auth-buttons">
        <router-link v-if="!isLoggedIn" to="/login" class="login-btn">
          Login
        </router-link>
        <button v-else @click="handleLogout" class="logout-btn">
          Logout
        </button>
      </div>
    </nav>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    const isLoggedIn = ref(false)

    const checkAuthStatus = () => {
      const token = localStorage.getItem('access_token')
      isLoggedIn.value = !!token
    }

    const handleAuthStateChanged = () => {
      checkAuthStatus()
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

    onMounted(() => {
      checkAuthStatus()
      window.addEventListener('auth-state-changed', handleAuthStateChanged)
    })

    onUnmounted(() => {
      window.removeEventListener('auth-state-changed', handleAuthStateChanged)
    })

    return {
      isLoggedIn,
      handleLogout
    }
  }
}
</script>

<style scoped>
.nav-container {
  background: #1a1a2e;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.nav-brand h1 {
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #e2e8f0;
  font-weight: 500;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: #8b5cf6;
  background: rgba(139, 92, 246, 0.1);
}

.nav-link.active {
  color: #8b5cf6;
  background: rgba(139, 92, 246, 0.15);
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.login-btn, .logout-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
}

.login-btn {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  color: white;
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.2);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.logout-btn {
  background: transparent;
  color: #e2e8f0;
  border: 2px solid #8b5cf6;
}

.logout-btn:hover {
  background: rgba(139, 92, 246, 0.1);
  transform: translateY(-2px);
  border-color: #6366f1;
}

@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .nav-links {
    order: 3;
    width: 100%;
    justify-content: space-between;
    gap: 0.5rem;
  }

  .nav-link {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }

  .auth-buttons {
    gap: 0.5rem;
  }

  .login-btn, .logout-btn {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}
</style>