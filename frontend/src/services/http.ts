import axios from 'axios'
import { useAuthStore } from '@/modules/auth/stores/authStore'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor — adjunta el token JWT si existe
http.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

// Response interceptor — maneja 401 global
http.interceptors.response.use(
  (response) => response,
  (error) => {
    // Si recibimos 401 y NO es del propio endpoint de login (para no recargar infinitamente o borrar el form)
    if (error.response?.status === 401 && !error.config.url?.includes('auth/login')) {
      const authStore = useAuthStore()
      authStore.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default http
