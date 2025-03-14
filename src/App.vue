<template>
  <div class="app-container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary" v-if="isLoggedIn">
      <div class="container">
        <router-link class="navbar-brand" to="/">Household Services</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <template v-if="userRole === 'admin'">
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/professionals">Professionals</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/services">Services</router-link>
              </li>
            </template>
            <template v-else-if="userRole === 'customer'">
              <li class="nav-item">
                <router-link class="nav-link" to="/services">Services</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/requests">My Requests</router-link>
              </li>
            </template>
            <template v-else-if="userRole === 'professional'">
              <li class="nav-item">
                <router-link class="nav-link" to="/professional/requests">Service Requests</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/professional/reviews">My Reviews</router-link>
              </li>
            </template>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth';
import { computed } from 'vue';

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();

    const isLoggedIn = computed(() => authStore.isLoggedIn);
    const userRole = computed(() => authStore.userRole);

    const logout = () => {
      authStore.logout();
    };

    return {
      isLoggedIn,
      userRole,
      logout
    };
  }
};
</script>

<style>
.app-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>