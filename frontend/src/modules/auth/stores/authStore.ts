import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, UserRole } from '@/types'
import http from '@/services/http'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('kambio_token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isOperator = computed(() => user.value?.role === 'operator')
  const hasRole = (role: UserRole) => user.value?.role === role

  async function login(email: string, password: string) {
    const { data } = await http.post<{ access_token: string }>('/api/v1/auth/login', {
      email,
      password,
    })
    token.value = data.access_token
    localStorage.setItem('kambio_token', data.access_token)
    await fetchMe()
  }

  async function fetchMe() {
    const { data } = await http.get<User>('/api/v1/auth/me')
    user.value = data
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('kambio_token')
  }

  return { token, user, isAuthenticated, isAdmin, isOperator, hasRole, login, fetchMe, logout }
})
