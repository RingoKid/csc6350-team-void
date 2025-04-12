import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from "../components/Login.vue";
import Dashboard from "../components/Dashboard.vue"; 
import SearchAndFilter from "../components/SearchAndFilter.vue";
import SinglePageView from "../views/SinglePageView.vue"
import ProjectList from "../components/ProjectList.vue";
import Blog from "../components/Blog.vue";
import CreateProject from '../components/CreateProject.vue'

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
        path: "/search",
        name: "search",
        component: SearchAndFilter,
      },
    
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
      path: '/project/:id', // ✅ 새로운 경로 추가
      name: 'SinglePageView',
      component: SinglePageView,
    },
    {
      path: '/projects',
      name: 'ProjectList',
      component: ProjectList,
    },
    {
      path: '/blog',
      name: 'Blog',
      component: Blog,
    },
    {
      path: '/create-project',
      name: 'create-project',
      component: CreateProject
    }
  ],
})

export default router
