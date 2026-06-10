import axios from 'axios';

// We do a lazy import to avoid SSR issues with zustand
function getAuthStore() {
  if (typeof window === 'undefined') return null;
  try {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const { useAuthStore } = require('@/store/auth');
    return useAuthStore.getState();
  } catch {
    return null;
  }
}

const api = axios.create({
  baseURL: typeof window !== 'undefined' ? '' : process.env.BACKEND_URL || 'http://localhost:5000',
  headers: { 'Content-Type': 'application/json' },
  timeout: 15000,
});

// Request interceptor: attach bearer token
api.interceptors.request.use((config) => {
  const store = getAuthStore();
  if (store?.accessToken) {
    config.headers.Authorization = `Bearer ${store.accessToken}`;
  }
  return config;
});

// Response interceptor: handle 401 and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const store = getAuthStore();
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      store?.refreshToken
    ) {
      originalRequest._retry = true;
      try {
        const { data } = await axios.post(
          `${process.env.BACKEND_URL || ''}/api/auth/refresh`,
          { refreshToken: store.refreshToken },
          { headers: { 'Content-Type': 'application/json' } }
        );
        store.setAuth(data);
        originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
        return api.request(originalRequest);
      } catch {
        store.clearAuth();
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;
