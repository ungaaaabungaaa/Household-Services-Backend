<template>
  <div>
    <h1 class="mb-4">Manage Professionals</h1>
    <div class="card">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div class="btn-group">
            <button
              class="btn"
              :class="filter === 'pending' ? 'btn-primary' : 'btn-outline-primary'"
              @click="filter = 'pending'"
            >
              Pending
            </button>
            <button
              class="btn"
              :class="filter === 'approved' ? 'btn-primary' : 'btn-outline-primary'"
              @click="filter = 'approved'"
            >
              Approved
            </button>
          </div>
          <div class="search-box">
            <input
              type="text"
              class="form-control"
              placeholder="Search professionals..."
              v-model="searchQuery"
            >
          </div>
        </div>

        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Service Type</th>
                <th>Experience</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="professional in filteredProfessionals" :key="professional.id">
                <td>{{ professional.name }}</td>
                <td>{{ professional.email }}</td>
                <td>{{ professional.service_type }}</td>
                <td>{{ professional.experience }} years</td>
                <td>
                  <span :class="professional.is_approved ? 'badge bg-success' : 'badge bg-warning'">
                    {{ professional.is_approved ? 'Approved' : 'Pending' }}
                  </span>
                </td>
                <td>
                  <button
                    v-if="!professional.is_approved"
                    class="btn btn-sm btn-success me-2"
                    @click="approveProfessional(professional.id)"
                  >
                    Approve
                  </button>
                  <button
                    class="btn btn-sm btn-info"
                    @click="viewDetails(professional)"
                  >
                    Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Professional Details Modal -->
    <div class="modal fade" id="professionalDetailsModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Professional Details</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" v-if="selectedProfessional">
              <div class="mb-3">
                <strong>Name:</strong> {{ selectedProfessional.name }}
              </div>
              <div class="mb-3">
                <strong>Email:</strong> {{ selectedProfessional.email }}
              </div>
              <div class="mb-3">
                <strong>Service Type:</strong> {{ selectedProfessional.service_type }}
              </div>
              <div class="mb-3">
                <strong>Experience:</strong> {{ selectedProfessional.experience }} years
              </div>
              <div class="mb-3">
                <strong>Description:</strong>
                <p>{{ selectedProfessional.description }}</p>
              </div>
            </div>
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
  name: 'ProfessionalsList',
  setup() {
    const professionals = ref([]);
    const filter = ref('pending');
    const searchQuery = ref('');
    const selectedProfessional = ref(null);
    let detailsModal = null;

    const filteredProfessionals = computed(() => {
      return professionals.value
        .filter(p => {
          const matchesFilter = filter.value === 'pending' ? !p.is_approved : p.is_approved;
          const matchesSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                              p.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                              p.service_type.toLowerCase().includes(searchQuery.value.toLowerCase());
          return matchesFilter && matchesSearch;
        });
    });

    const fetchProfessionals = async () => {
      try {
        const response = await axios.get('/api/admin/professionals');
        professionals.value = response.data;
      } catch (error) {
        console.error('Error fetching professionals:', error);
      }
    };

    const approveProfessional = async (id) => {
      try {
        await axios.post(`/api/admin/professionals/${id}/approve`);
        await fetchProfessionals();
      } catch (error) {
        console.error('Error approving professional:', error);
      }
    };

    const viewDetails = (professional) => {
      selectedProfessional.value = professional;
      detailsModal.show();
    };

    onMounted(() => {
      fetchProfessionals();
      detailsModal = new Modal(document.getElementById('professionalDetailsModal'));
    });

    return {
      professionals,
      filter,
      searchQuery,
      selectedProfessional,
      filteredProfessionals,
      approveProfessional,
      viewDetails
    };
  }
};
</script>