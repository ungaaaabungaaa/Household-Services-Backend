<template>
  <div>
    <h1 class="mb-4">My Service Requests</h1>
    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Service</th>
                <th>Status</th>
                <th>Date</th>
                <th>Professional</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in requests" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>
                  <span :class="getStatusBadgeClass(request.status)">
                    {{ request.status }}
                  </span>
                </td>
                <td>
                  {{ request.preferred_date }}
                  <br>
                  <small class="text-muted">{{ request.preferred_time }}</small>
                </td>
                <td>
                  {{ request.professional_name || 'Not assigned' }}
                </td>
                <td>
                  <button
                    class="btn btn-sm btn-info me-2"
                    @click="viewDetails(request)"
                  >
                    Details
                  </button>
                  <button
                    v-if="request.status === 'completed' && !request.has_review"
                    class="btn btn-sm btn-primary"
                    @click="showReviewModal(request)"
                  >
                    Add Review
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
              <strong>Address:</strong>
              <p>{{ selectedRequest.address }}</p>
            </div>
            <div class="mb-3">
              <strong>PIN Code:</strong> {{ selectedRequest.pin_code }}
            </div>
            <div class="mb-3">
              <strong>Status:</strong>
              <span :class="getStatusBadgeClass(selectedRequest.status)">
                {{ selectedRequest.status }}
              </span>
            </div>
            <div v-if="selectedRequest.completion_notes" class="mb-3">
              <strong>Completion Notes:</strong>
              <p>{{ selectedRequest.completion_notes }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Review Modal -->
    <div class="modal fade" id="reviewModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Review</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitReview">
              <div class="mb-3">
                <label class="form-label">Overall Rating</label>
                <div class="rating-input">
                  <i
                    v-for="n in 5"
                    :key="n"
                    class="bi"
                    :class="n <= reviewForm.rating ? 'bi-star-fill' : 'bi-star'"
                    @click="reviewForm.rating = n"
                  ></i>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Punctuality</label>
                <input
                  type="range"
                  class="form-range"
                  min="1"
                  max="5"
                  v-model="reviewForm.aspects.punctuality"
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Professionalism</label>
                <input
                  type="range"
                  class="form-range"
                  min="1"
                  max="5"
                  v-model="reviewForm.aspects.professionalism"
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Work Quality</label>
                <input
                  type="range"
                  class="form-range"
                  min="1"
                  max="5"
                  v-model="reviewForm.aspects.work_quality"
                >
              </div>
              <div class="mb-3">
                <label for="comment" class="form-label">Comment</label>
                <textarea
                  class="form-control"
                  id="comment"
                  v-model="reviewForm.comment"
                  rows="3"
                ></textarea>
              </div>
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  Submit Review
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
  name: 'RequestsList',
  setup() {
    const requests = ref([]);
    const selectedRequest = ref(null);
    const reviewForm = ref({
      service_request_id: null,
      rating: 0,
      comment: '',
      aspects: {
        punctuality: 3,
        professionalism: 3,
        work_quality: 3
      }
    });
    let detailsModal = null;
    let reviewModal = null;

    const getStatusBadgeClass = (status) => {
      const classes = {
        pending: 'badge bg-warning',
        accepted: 'badge bg-info',
        completed: 'badge bg-success',
        cancelled: 'badge bg-danger'
      };
      return classes[status] || 'badge bg-secondary';
    };

    const fetchRequests = async () => {
      try {
        const response = await axios.get('/api/customer/service-requests');
        requests.value = response.data;
      } catch (error) {
        console.error('Error fetching requests:', error);
      }
    };

    const viewDetails = (request) => {
      selectedRequest.value = request;
      detailsModal.show();
    };

    const showReviewModal = (request) => {
      reviewForm.value.service_request_id = request.id;
      reviewForm.value.rating = 0;
      reviewForm.value.comment = '';
      reviewForm.value.aspects = {
        punctuality: 3,
        professionalism: 3,
        work_quality: 3
      };
      reviewModal.show();
    };

    const submitReview = async () => {
      try {
        await axios.post('/api/customer/reviews', reviewForm.value);
        await fetchRequests();
        reviewModal.hide();
      } catch (error) {
        console.error('Error submitting review:', error);
      }
    };

    onMounted(() => {
      fetchRequests();
      detailsModal = new Modal(document.getElementById('requestDetailsModal'));
      reviewModal = new Modal(document.getElementById('reviewModal'));
    });

    return {
      requests,
      selectedRequest,
      reviewForm,
      getStatusBadgeClass,
      viewDetails,
      showReviewModal,
      submitReview
    };
  }
};
</script>

<style scoped>
.rating-input {
  font-size: 1.5rem;
  color: #ffc107;
  cursor: pointer;
}
.rating-input i {
  margin-right: 0.25rem;
}
</style>