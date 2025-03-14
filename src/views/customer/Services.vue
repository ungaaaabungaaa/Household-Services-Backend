<template>
  <div>
    <h1 class="mb-4">Available Services</h1>
    <div class="row mb-4">
      <div class="col-md-6">
        <input
          type="text"
          class="form-control"
          placeholder="Search services..."
          v-model="searchQuery"
        >
      </div>
      <div class="col-md-3">
        <select class="form-select" v-model="selectedCategory">
          <option value="">All Categories</option>
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>
      <div class="col-md-3">
        <input
          type="text"
          class="form-control"
          placeholder="PIN Code"
          v-model="pinCode"
        >
      </div>
    </div>

    <div class="row">
      <div class="col-md-4 mb-4" v-for="service in filteredServices" :key="service.id">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ service.name }}</h5>
            <p class="card-text">{{ service.description }}</p>
            <div class="mb-3">
              <small class="text-muted">
                Category: {{ service.category }}
              </small>
            </div>
            <div class="d-flex justify-content-between align-items-center mb-3">
              <div>
                <strong>${{ service.base_price }}</strong>
                <small class="text-muted">
                  ({{ service.required_time }} minutes)
                </small>
              </div>
              <div class="rating">
                <i class="bi bi-star-fill text-warning"></i>
                {{ service.average_rating.toFixed(1) }}
              </div>
            </div>
            <button
              class="btn btn-primary w-100"
              @click="requestService(service)"
            >
              Request Service
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Request Service Modal -->
    <div class="modal fade" id="requestServiceModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Request Service</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitRequest">
              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea
                  class="form-control"
                  id="description"
                  v-model="requestForm.description"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="preferred_date" class="form-label">Preferred Date</label>
                <input
                  type="date"
                  class="form-control"
                  id="preferred_date"
                  v-model="requestForm.preferred_date"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="preferred_time" class="form-label">Preferred Time</label>
                <input
                  type="time"
                  class="form-control"
                  id="preferred_time"
                  v-model="requestForm.preferred_time"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <textarea
                  class="form-control"
                  id="address"
                  v-model="requestForm.address"
                  rows="2"
                  required
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="request_pin_code" class="form-label">PIN Code</label>
                <input
                  type="text"
                  class="form-control"
                  id="request_pin_code"
                  v-model="requestForm.pin_code"
                  required
                >
              </div>
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  Submit Request
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { Modal } from 'bootstrap';

export default {
  name: 'ServicesList',
  setup() {
    const services = ref([]);
    const searchQuery = ref('');
    const selectedCategory = ref('');
    const pinCode = ref('');
    const categories = ref([]);
    const requestForm = ref({
      service_id: null,
      description: '',
      preferred_date: '',
      preferred_time: '',
      address: '',
      pin_code: ''
    });
    let requestModal = null;

    const filteredServices = computed(() => {
      return services.value.filter(service => {
        const matchesSearch = service.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                            service.description.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesCategory = !selectedCategory.value || service.category === selectedCategory.value;
        return matchesSearch && matchesCategory;
      });
    });

    const fetchServices = async () => {
      try {
        const response = await axios.get('/api/services');
        services.value = response.data;
        categories.value = [...new Set(services.value.map(s => s.category))];
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    };

    const requestService = (service) => {
      requestForm.value = {
        service_id: service.id,
        description: '',
        preferred_date: '',
        preferred_time: '',
        address: '',
        pin_code: pinCode.value
      };
      requestModal.show();
    };

    const submitRequest = async () => {
      try {
        await axios.post('/api/customer/service-request', requestForm.value);
        requestModal.hide();
        // Show success message
      } catch (error) {
        console.error('Error submitting request:', error);
      }
    };

    onMounted(() => {
      fetchServices();
      requestModal = new Modal(document.getElementById('requestServiceModal'));
    });

    return {
      services,
      searchQuery,
      selectedCategory,
      pinCode,
      categories,
      filteredServices,
      requestForm,
      requestService,
      submitRequest
    };
  }
};
</script>

<style scoped>
.rating {
  color: #ffc107;
}
</style>