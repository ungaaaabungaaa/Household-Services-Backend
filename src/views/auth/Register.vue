<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card shadow">
        <div class="card-body">
          <h2 class="text-center mb-4">Register</h2>
          <div class="mb-4">
            <div class="btn-group w-100">
              <button
                class="btn"
                :class="role === 'customer' ? 'btn-primary' : 'btn-outline-primary'"
                @click="role = 'customer'"
              >
                Customer
              </button>
              <button
                class="btn"
                :class="role === 'professional' ? 'btn-primary' : 'btn-outline-primary'"
                @click="role = 'professional'"
              >
                Professional
              </button>
            </div>
          </div>
          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label for="name" class="form-label">Name</label>
              <input
                type="text"
                class="form-control"
                id="name"
                v-model="formData.name"
                required
              >
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <input
                type="email"
                class="form-control"
                id="email"
                v-model="formData.email"
                required
              >
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="formData.password"
                required
              >
            </div>
            
            <template v-if="role === 'customer'">
              <div class="mb-3">
                <label for="pin_code" class="form-label">PIN Code</label>
                <input
                  type="text"
                  class="form-control"
                  id="pin_code"
                  v-model="formData.pin_code"
                  required
                >
              </div>
            </template>

            <template v-if="role === 'professional'">
              <div class="mb-3">
                <label for="service_type" class="form-label">Service Type</label>
                <input
                  type="text"
                  class="form-control"
                  id="service_type"
                  v-model="formData.service_type"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="experience" class="form-label">Experience (years)</label>
                <input
                  type="number"
                  class="form-control"
                  id="experience"
                  v-model="formData.experience"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea
                  class="form-control"
                  id="description"
                  v-model="formData.description"
                  rows="3"
                  required
                ></textarea>
              </div>
            </template>

            <button type="submit" class="btn btn-primary w-100">Register</button>
          </form>
          <div class="mt-3 text-center">
            <router-link to="/login">Already have an account? Login</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

export default {
  name: 'Register',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const role = ref('customer');
    const formData = reactive({
      name: '',
      email: '',
      password: '',
      pin_code: '',
      service_type: '',
      experience: '',
      description: ''
    });

    const handleRegister = async () => {
      let success;
      if (role.value === 'customer') {
        success = await authStore.registerCustomer({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          pin_code: formData.pin_code
        });
      } else {
        success = await authStore.registerProfessional({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          service_type: formData.service_type,
          experience: parseInt(formData.experience),
          description: formData.description
        });
      }

      if (success) {
        router.push('/login');
      }
    };

    return {
      role,
      formData,
      handleRegister
    };
  }
};
</script>