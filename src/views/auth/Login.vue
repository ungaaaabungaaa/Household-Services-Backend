<template>
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
      <div class="card shadow">
        <div class="card-body">
          <h2 class="text-center mb-4">Login</h2>
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <input
                type="email"
                class="form-control"
                id="email"
                v-model="email"
                required
              >
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="password"
                required
              >
            </div>
            <button type="submit" class="btn btn-primary w-100">Login</button>
          </form>
          <div class="mt-3 text-center">
            <router-link to="/register">Don't have an account? Register</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

export default {
  name: 'Login',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const email = ref('');
    const password = ref('');

    const handleLogin = async () => {
      const success = await authStore.login(email.value, password.value);
      if (success) {
        const role = authStore.userRole;
        switch (role) {
          case 'admin':
            router.push('/admin/dashboard');
            break;
          case 'customer':
            router.push('/services');
            break;
          case 'professional':
            router.push('/professional/requests');
            break;
        }
      }
    };

    return {
      email,
      password,
      handleLogin
    };
  }
};
</script>