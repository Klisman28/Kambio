import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/authStore'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/modules/auth/pages/LoginPage.vue'),
      meta: { public: true },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/modules/dashboard/pages/DashboardPage.vue'),
      meta: { requiresAuth: true },
    },
    // Fase 1
    {
      path: '/clients',
      name: 'clients',
      component: () => import('@/modules/clients/pages/ClientsPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/transactions',
      name: 'transactions',
      component: () => import('@/modules/transactions/pages/TransactionsPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/ledger/:clientId',
      name: 'ledger',
      component: () => import('@/modules/ledger/pages/LedgerPage.vue'),
      meta: { requiresAuth: true },
    },
    // Fase 2
    {
      path: '/cash',
      name: 'cash',
      component: () => import('@/modules/cash/pages/CashPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/reports',
      name: 'reports',
      component: () => import('@/modules/reports/pages/ReportsPage.vue'),
      meta: { requiresAuth: true },
    },
    // Redirecciones
    { path: '/', redirect: '/dashboard' },
    { path: '/:pathMatch(.*)*', redirect: '/dashboard' },
  ],
})

// Navigation guard: protege rutas autenticadas
router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.name === 'login' && authStore.isAuthenticated) {
    return { name: 'dashboard' }
  }
})

export default router
