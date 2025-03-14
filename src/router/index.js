import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// Auth Views
import Login from '../views/auth/Login.vue';
import Register from '../views/auth/Register.vue';

// Admin Views
import AdminDashboard from '../views/admin/Dashboard.vue';
import ProfessionalsList from '../views/admin/Professionals.vue';
import ServiceManagement from '../views/admin/Services.vue';

// Customer Views
import ServicesList from '../views/customer/Services.vue';
import RequestsList from '../views/customer/Requests.vue';

// Professional Views
import ProfessionalRequests from '../views/professional/Requests.vue';
import ProfessionalReviews from '../views/professional/Reviews.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/professionals',
    name: 'ProfessionalsList',
    component: ProfessionalsList,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/services',
    name: 'ServiceManagement',
    component: ServiceManagement,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/services',
    name: 'ServicesList',
    component: ServicesList,
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/requests',
    name: 'RequestsList',
    component: RequestsList,
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/professional/requests',
    name: 'ProfessionalRequests',
    component: ProfessionalRequests,
    meta: { requiresAuth: true, role: 'professional' }
  },
  {
    path: '/professional/reviews',
    name: 'ProfessionalReviews',
    component: ProfessionalReviews,
    meta: { requiresAuth: true, role: 'professional' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login');
  } else if (to.meta.role && to.meta.role !== authStore.userRole) {
    next('/');
  } else {
    next();
  }
});

export default router;