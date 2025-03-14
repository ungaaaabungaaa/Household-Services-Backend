import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    userRole: localStorage.getItem('userRole') || null
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
    async login(email, password) {
      try {
        const response = await axios.post('/api/auth/login', { email, password });
        this.token = response.data.access_token;
        this.userRole = response.data.role;
        localStorage.setItem('token', this.token);
        localStorage.setItem('userRole', this.userRole);
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        return true;
      } catch (error) {
        console.error('Login failed:', error);
        return false;
      }
    },

    async registerCustomer(userData) {
      try {
        await axios.post('/api/auth/register/customer', userData);
        return true;
      } catch (error) {
        console.error('Customer registration failed:', error);
        return false;
      }
    },

    async registerProfessional(userData) {
      try {
        await axios.post('/api/auth/register/professional', userData);
        return true;
      } catch (error) {
        console.error('Professional registration failed:', error);
        return false;
      }
    },

    logout() {
      this.token = null;
      this.userRole = null;
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      delete axios.defaults.headers.common['Authorization'];
    }
  }
});