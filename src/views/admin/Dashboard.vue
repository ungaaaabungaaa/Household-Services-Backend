<template>
  <div>
    <h1 class="mb-4">Admin Dashboard</h1>
    <div class="row">
      <div class="col-md-4">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">Pending Professionals</h5>
            <h2 class="card-text">{{ stats.pendingProfessionals }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">Total Services</h5>
            <h2 class="card-text">{{ stats.totalServices }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">Active Requests</h5>
            <h2 class="card-text">{{ stats.activeRequests }}</h2>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Recent Service Requests</h5>
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>Status</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="request in recentRequests" :key="request.id">
                    <td>{{ request.id }}</td>
                    <td>{{ request.service_name }}</td>
                    <td>
                      <span :class="getStatusBadgeClass(request.status)">
                        {{ request.status }}
                      </span>
                    </td>
                    <td>{{ formatDate(request.created_at) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Service Categories Performance</h5>
            <Bar v-if="chartData.datasets[0].data.length > 0" :data="chartData" :options="chartOptions" />
            <div v-else class="text-center py-4">
              <p class="text-muted">No data available</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import axios from 'axios';
import moment from 'moment';
import { useToast } from 'vue-toastification';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default {
  name: 'AdminDashboard',
  components: { Bar },
  setup() {
    const stats = ref({
      pendingProfessionals: 0,
      totalServices: 0,
      activeRequests: 0
    });

    const recentRequests = ref([]);
    const toast = useToast();

    const chartData = ref({
      labels: ['Plumbing', 'Electrical', 'Cleaning', 'Carpentry', 'Painting'],
      datasets: [{
        label: 'Completed Services',
        data: [0, 0, 0, 0, 0],
        backgroundColor: 'rgba(75, 192, 192, 0.5)'
      }]
    });

    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      },
      plugins: {
        legend: {
          display: true
        }
      }
    };

    const getStatusBadgeClass = (status) => {
      const classes = {
        pending: 'badge bg-warning',
        accepted: 'badge bg-info',
        completed: 'badge bg-success',
        cancelled: 'badge bg-danger'
      };
      return classes[status] || 'badge bg-secondary';
    };

    const formatDate = (date) => {
      return moment(date).format('MMM D, YYYY');
    };

    const fetchDashboardData = async () => {
      try {
        const [statsRes, requestsRes, performanceRes] = await Promise.all([
          axios.get('/admin/stats'),
          axios.get('/admin/recent-requests'),
          axios.get('/admin/service-performance')
        ]);

        stats.value = statsRes.data;
        recentRequests.value = requestsRes.data;
        chartData.value.datasets[0].data = performanceRes.data.map(item => item.count);
      } catch (error) {
        toast.error('Error fetching dashboard data');
        console.error('Error fetching dashboard data:', error);
      }
    };

    onMounted(() => {
      fetchDashboardData();
    });

    return {
      stats,
      recentRequests,
      chartData,
      chartOptions,
      getStatusBadgeClass,
      formatDate
    };
  }
};
</script>