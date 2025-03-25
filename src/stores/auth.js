import { defineStore } from 'pinia';
import axios from 'axios';
import { useToast } from 'vue-toastification';

const toast = useToast();

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
        toast.success('Successfully logged in');
        return true;
      } catch (error) {
        const message = error.response?.data?.error || 'Login failed';
        toast.error(message);
        return false;
      }
    },

    async registerCustomer(userData) {
      try {
        await axios.post('/api/auth/register/customer', {
          email: userData.email,
          password: userData.password,
          name: userData.name,
          pin_code: userData.pin_code
        });
        toast.success('Registration successful! Please login.');
        return true;
      } catch (error) {
        const message = error.response?.data?.error || 'Customer registration failed';
        toast.error(message);
        return false;
      }
    },

    async registerProfessional(userData) {
      try {
        await axios.post('/api/auth/register/professional', {
          email: userData.email,
          password: userData.password,
          name: userData.name,
          service_type: userData.service_type,
          experience: Number(userData.experience),
          description: userData.description
        });
        toast.success('Registration successful! Please wait for admin approval.');
        return true;
      } catch (error) {
        const message = error.response?.data?.error || 'Professional registration failed';
        toast.error(message);
        return false;
      }
    },

    logout() {
      this.token = null;
      this.userRole = null;
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      delete axios.defaults.headers.common['Authorization'];
      toast.info('Logged out successfully');
    }
  }
});