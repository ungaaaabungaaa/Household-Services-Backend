<template>
  <div>
    <h1 class="mb-4">Manage Services</h1>
    <div class="row mb-4">
      <div class="col">
        <button class="btn btn-primary" @click="showAddServiceModal">
          Add New Service
        </button>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Name</th>
                <th>Category</th>
                <th>Base Price</th>
                <th>Required Time</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="service in services" :key="service.id">
                <td>{{ service.name }}</td>
                <td>{{ service.category }}</td>
                <td>${{ service.base_price }}</td>
                <td>{{ service.required_time }} minutes</td>
                <td>
                  <button
                    class="btn btn-sm btn-info me-2"
                    @click="editService(service)"
                  >
                    Edit
                  </button>
                  <button
                    class="btn btn-sm btn-danger"
                    @click="deleteService(service.id)"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Add/Edit Service Modal -->
    <div class="modal fade" id="serviceModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditing ? 'Edit Service' : 'Add New Service' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveService">
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="name"
                  v-model="serviceForm.name"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="category" class="form-label">Category</label>
                <input
                  type="text"
                  class="form-control"
                  id="category"
                  v-model="serviceForm.category"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea
                  class="form-control"
                  id="description"
                  v-model="serviceForm.description"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="base_price" class="form-label">Base Price ($)</label>
                <input
                  type="number"
                  class="form-control"
                  id="base_price"
                  v-model="serviceForm.base_price"
                  step="0.01"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="required_time" class="form-label">Required Time (minutes)</label>
                <input
                  type="number"
                  class="form-control"
                  id="required_time"
                  v-model="serviceForm.required_time"
                  required
                >
              </div>
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  {{ isEditing ? 'Update' : 'Create' }}
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
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Modal } from 'bootstrap';

export default {
  name: 'ServiceManagement',
  setup() {
    const services = ref([]);
    const isEditing = ref(false);
    const serviceForm = ref({
      id: null,
      name: '',
      category: '',
      description: '',
      base_price: '',
      required_time: ''
    });
    let serviceModal = null;

    const fetchServices = async () => {
      try {
        const response = await axios.get('/api/services');
        services.value = response.data;
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    };

    const showAddServiceModal = () => {
      isEditing.value = false;
      serviceForm.value = {
        id: null,
        name: '',
        category: '',
        description: '',
        base_price: '',
        required_time: ''
      };
      serviceModal.show();
    };

    const editService = (service) => {
      isEditing.value = true;
      serviceForm.value = { ...service };
      serviceModal.show();
    };

    const saveService = async () => {
      try {
        if (isEditing.value) {
          await axios.put(`/api/admin/services/${serviceForm.value.id}`, serviceForm.value);
        } else {
          await axios.post('/api/admin/services', serviceForm.value);
        }
        await fetchServices();
        serviceModal.hide();
      } catch (error) {
        console.error('Error saving service:', error);
      }
    };

    const deleteService = async (id) => {
      if (confirm('Are you sure you want to delete this service?')) {
        try {
          await axios.delete(`/api/admin/services/${id}`);
          await fetchServices();
        } catch (error) {
          console.error('Error deleting service:', error);
        }
      }
    };

    onMounted(() => {
      fetchServices();
      serviceModal = new Modal(document.getElementById('serviceModal'));
    });

    return {
      services,
      isEditing,
      serviceForm,
      showAddServiceModal,
      editService,
      saveService,
      deleteService
    };
  }
};
</script>