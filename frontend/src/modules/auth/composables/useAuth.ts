import { useAuthStore } from '@/modules/auth/stores/authStore'
import { useRouter } from 'vue-router'

export function useAuth() {
  const authStore = useAuthStore()
  const router = useRouter()

  async function login(email: string, password: string) {
    await authStore.login(email, password)
    await router.push('/dashboard')
  }

  async function logout() {
    authStore.logout()
    await router.push('/login')
  }

  return {
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated,
    isAdmin: authStore.isAdmin,
    isOperator: authStore.isOperator,
    hasRole: authStore.hasRole,
    login,
    logout,
  }
}
