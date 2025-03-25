import { createApp } from 'vue';
import { createPinia } from 'pinia';
import Toast from 'vue-toastification';
import App from './App.vue';
import router from './router';
import axios from 'axios';

// Styles
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'vue-toastification/dist/index.css';
import './assets/main.css';

// Bootstrap JS
import 'bootstrap';

// Axios default config
axios.defaults.baseURL = '/api';
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

const app = createApp(App);

// Toast configuration
const toastOptions = {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: true,
  closeButton: 'button',
  icon: true,
  rtl: false
};

app.use(createPinia());
app.use(router);
app.use(Toast, toastOptions);

app.mount('#app');