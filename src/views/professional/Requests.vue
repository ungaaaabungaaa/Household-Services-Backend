<template>
  <div>
    <h1 class="mb-4">Service Requests</h1>
    <div class="row mb-4">
      <div class="col">
        <div class="btn-group">
          <button
            class="btn"
            :class="filter === 'available' ? 'btn-primary' : 'btn-outline-primary'"
            @click="filter = 'available'"
          >
            Available
          </button>
          <button
            class="btn"
            :class="filter === 'accepted' ? 'btn-primary' : 'btn-outline-primary'"
            @click="filter = 'accepted'"
          >
            Accepted
          </button>
          <button
            class="btn"
            :class="filter === 'completed' ? 'btn-primary' : 'btn-outline-primary'"
            @click="filter = 'completed'"
          >
            Completed
          </button>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>Description</th>
                <th>Date & Time</th>
                <th>Location</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in filteredRequests" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.description }}</td>
                <td>
                  {{ request.preferred_date }}
                  <br>
                  <small class="text-muted">{{ request.preferred_time }}</small>
                </td>
                <td>
                  <span class="badge bg-secondary">{{ request.pin_code }}</span>
                </td>
                <td>
                  <button
                    v-if="filter === 'available'"
                    class="btn btn-sm btn-success me-2"
                    @click="acceptRequest(request.id)"
                  >
                    Accept
                  </button>
                  <button
                    v-if="filter === 'accepted'"
                    class="btn btn-sm btn-primary me-2"
                    @click="showCompleteModal(request)"
                  >
                    Complete
                  </button>
                  <button
                    class="btn btn-sm btn-info"
                    @click="viewDetails(request)"
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

    <!-- Request Details Modal -->
    <div class="modal fade" id="requestDetailsModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Request Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedRequest">
            <div class="mb-3">
              <strong>Service:</strong> {{ selectedRequest.service_name }}
            </div>
            <div class="mb-3">
              <strong>Description:</strong>
              <p>{{ selectedRequest.description }}</p>
            </div>
            <div class="mb-3">
              <strong>Customer:</strong> {{ selectedRequest.customer_name }}
            </div>
            <div class="mb-3">
              <strong>Address:</strong>
              <p>{{ selectedRequest.address }}</p>
            </div>
            <div class="mb-3">
              <strong>PIN Code:</strong> {{ selectedRequest.pin_code }}
            </div>
            <div class="mb-3">
              <strong>Date:</strong> {{ selectedRequest.preferred_date }}
            </div>
            <div class="mb-3">
              <strong>Time:</strong> {{ selectedRequest.preferred_time }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Complete Request Modal -->
    <div class="modal fade" id="completeRequestModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Complete Request</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="completeRequest">
              <div class="mb-3">
                <label for="notes" class="form-label">Completion Notes</label>
                <textarea
                  class="form-control"
                  id="notes"
                  v-model="completionForm.notes"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="duration" class="form-label">Duration (minutes)</label>
                <input
                  type="number"
                  class="form-control"
                  id="duration"
                  v-model="completionForm.duration"
                  required
                >
              </div>
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  Complete Request
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
  name: 'ProfessionalRequests',
  setup() {
    const requests = ref([]);
    const filter = ref('available');
    const selectedRequest = ref(null);
    const completionForm = ref({
      request_id: null,
      notes: '',
      duration: ''
    });
    let detailsModal = null;
    let completeModal = null;

    const filteredRequests = computed(() => {
      const statusMap = {
        available: 'pending',
        accepted: 'accepted',
        completed: 'completed'
      };
      return requests.value.filter(r => r.status === statusMap[filter.value]);
    });

    const fetchRequests = async () => {
      try {
        const response = await axios.get('/api/professional/requests');
        requests.value = response.data;
      } catch (error) {
        console.error('Error fetching requests:', error);
      }
    };

    const acceptRequest = async (id) => {
      try {
        await axios.post(`/api/professional/requests/${id}/accept`);
        await fetchRequests();
      } catch (error) {
        console.error('Error accepting request:', error);
      }
    };

    const viewDetails = (request) => {
      selectedRequest.value = request;
      detailsModal.show();
    };

    const showCompleteModal = (request) => {
      completionForm.value = {
        request_id: request.id,
        notes: '',
        duration: ''
      };
      completeModal.show();
    };

    const completeRequest = async () => {
      try {
        await axios.post(`/api/professional/requests/${completionForm.value.request_id}/complete`, {
          notes: completionForm.value.notes,
          duration: parseInt(completionForm.value.duration)
        });
        await fetchRequests();
        completeModal.hide();
      } catch (error) {
        console.error('Error completing request:', error);
      }
    };

    onMounted(() => {
      fetchRequests();
      detailsModal = new Modal(document.getElementById('requestDetailsModal'));
      completeModal = new Modal(document.getElementById('completeRequestModal'));
    });

    return {
      requests,
      filter,
      selectedRequest,
      completionForm,
      filteredRequests,
      acceptRequest,
      viewDetails,
      showCompleteModal,
      completeRequest
    };
  }
};
</script>