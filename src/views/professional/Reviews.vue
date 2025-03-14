<template>
  <div>
    <h1 class="mb-4">My Reviews</h1>
    <div class="row">
      <div class="col-md-4">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">Overall Rating</h5>
            <div class="display-4 text-center mb-3">
              {{ averageRating.toFixed(1) }}
              <small class="text-muted">/5</small>
            </div>
            <div class="text-center">
              <i
                v-for="n in 5"
                :key="n"
                class="bi"
                :class="n <= Math.round(averageRating) ? 'bi-star-fill' : 'bi-star'"
              ></i>
            </div>
            <div class="text-center text-muted mt-2">
              Based on {{ reviews.length }} reviews
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Rating Breakdown</h5>
            <div class="mb-3">
              <label class="d-flex justify-content-between">
                <span>Punctuality</span>
                <span>{{ averageAspects.punctuality.toFixed(1) }}/5</span>
              </label>
              <div class="progress">
                <div
                  class="progress-bar bg-success"
                  :style="{ width: (averageAspects.punctuality / 5 * 100) + '%' }"
                ></div>
              </div>
            </div>
            <div class="mb-3">
              <label class="d-flex justify-content-between">
                <span>Professionalism</span>
                <span>{{ averageAspects.professionalism.toFixed(1) }}/5</span>
              </label>
              <div class="progress">
                <div
                  class="progress-bar bg-success"
                  :style="{ width: (averageAspects.professionalism / 5 * 100) + '%' }"
                ></div>
              </div>
            </div>
            <div>
              <label class="d-flex justify-content-between">
                <span>Work Quality</span>
                <span>{{ averageAspects.workQuality.toFixed(1) }}/5</span>
              </label>
              <div class="progress">
                <div
                  class="progress-bar bg-success"
                  :style="{ width: (averageAspects.workQuality / 5 * 100) + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-8">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title mb-4">Recent Reviews</h5>
            <div class="review-list">
              <div v-for="review in reviews" :key="review.id" class="review-item mb-4">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <div class="rating mb-1">
                      <i
                        v-for="n in 5"
                        :key="n"
                        class="bi"
                        :class="n <= review.rating ? 'bi-star-fill' : 'bi-star'"
                      ></i>
                    </div>
                    <div class="text-muted">
                      {{ new Date(review.created_at).toLocaleDateString() }}
                    </div>
                  </div>
                  <div class="service-info text-end">
                    <div class="fw-bold">{{ review.service_name }}</div>
                    <small class="text-muted">Request #{{ review.service_request_id }}</small>
                  </div>
                </div>
                <p class="review-comment mb-3">{{ review.comment }}</p>
                <div class="aspects">
                  <span class="badge bg-light text-dark me-2">
                    Punctuality: {{ review.aspects.punctuality }}/5
                  </span>
                  <span class="badge bg-light text-dark me-2">
                    Professionalism: {{ review.aspects.professionalism }}/5
                  </span>
                  <span class="badge bg-light text-dark">
                    Work Quality: {{ review.aspects.work_quality }}/5
                  </span>
                </div>
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

export default {
  name: 'ProfessionalReviews',
  setup() {
    const reviews = ref([]);

    const averageRating = computed(() => {
      if (!reviews.value.length) return 0;
      const sum = reviews.value.reduce((acc, review) => acc + review.rating, 0);
      return sum / reviews.value.length;
    });

    const averageAspects = computed(() => {
      if (!reviews.value.length) return { punctuality: 0, professionalism: 0, workQuality: 0 };
      
      const sum = reviews.value.reduce((acc, review) => ({
        punctuality: acc.punctuality + review.aspects.punctuality,
        professionalism: acc.professionalism + review.aspects.professionalism,
        workQuality: acc.workQuality + review.aspects.work_quality
      }), { punctuality: 0, professionalism: 0, workQuality: 0 });

      return {
        punctuality: sum.punctuality / reviews.value.length,
        professionalism: sum.professionalism / reviews.value.length,
        workQuality: sum.workQuality / reviews.value.length
      };
    });

    const fetchReviews = async () => {
      try {
        const response = await axios.get('/api/professional/reviews');
        reviews.value = response.data;
      } catch (error) {
        console.error('Error fetching reviews:', error);
      }
    };

    onMounted(() => {
      fetchReviews();
    });

    return {
      reviews,
      averageRating,
      averageAspects
    };
  }
};
</script>

<style scoped>
.rating {
  color: #ffc107;
}
.review-item {
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 1rem;
}
.review-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
.aspects .badge {
  font-weight: normal;
}
</style>