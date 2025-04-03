import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from "../components/Login.vue";
import Dashboard from "../components/Dashboard.vue";
import SinglePageView from "../views/SinglePageView.vue"


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
      
    },
    { 
      path: "/login", 
      name: "login", 
      component: Login },
    
      { 
      path: "/dashboard", 
      name: "dashboard", 
      component: Dashboard, 
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem("access_token");
        if (token) {
          next();
        } else {
          next("/login");
        }
      },
      
    }, // Example protected page
    {
      path: '/single-page', // ✅ 새로운 경로 추가
      name: 'SinglePageView',
      component: SinglePageView,
    },
  ],
})

export default router
