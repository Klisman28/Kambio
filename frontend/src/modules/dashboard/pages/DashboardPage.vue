<template>
  <div class="py-6 space-y-8">
    <!-- Header -->
    <div class="flex flex-col gap-2 md:items-center md:flex-row md:justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-foreground">Dashboard</h1>
        <p class="text-muted">Bienvenido, {{ user?.full_name }} — Resumen General</p>
      </div>
      <div class="flex gap-3">
        <router-link to="/transactions">
          <Button>+ Nueva Transacción</Button>
        </router-link>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="py-10 text-center text-muted">Cargando dashboard...</div>

    <template v-else-if="summary">
      <!-- Cash Status Banner -->
      <div v-if="!summary.cash.is_open" class="bg-warning-light border border-warning/30 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="flex items-center gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-warning-dark"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          <p class="text-sm font-medium text-warning-dark">No hay caja abierta. Abre una sesión para registrar transacciones.</p>
        </div>
        <router-link to="/cash">
          <Button size="sm" variant="outline" class="border-warning-dark text-warning-dark hover:bg-warning-light">Ir a Caja</Button>
        </router-link>
      </div>

      <!-- Stats Row -->
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
        <!-- Caja MXN -->
        <div class="p-6 rounded-xl bg-card shadow-sm ring-1 ring-border transition-shadow hover:shadow-md">
          <div class="flex items-center justify-between">
            <p class="text-sm font-medium text-muted">Saldo Caja MXN</p>
            <div class="w-9 h-9 rounded-lg bg-primary-light flex items-center justify-center">
              <span class="text-primary-dark font-bold text-sm">$</span>
            </div>
          </div>
          <div class="mt-3">
            <h3 class="text-2xl font-bold text-foreground font-mono">$ {{ fmt(summary.cash.opening_mxn) }}</h3>
            <p class="text-xs text-muted mt-1">{{ summary.cash.is_open ? 'Caja abierta' : 'Sin sesión' }}</p>
          </div>
        </div>

        <!-- Caja GTQ -->
        <div class="p-6 rounded-xl bg-card shadow-sm ring-1 ring-border transition-shadow hover:shadow-md">
          <div class="flex items-center justify-between">
            <p class="text-sm font-medium text-muted">Saldo Caja GTQ</p>
            <div class="w-9 h-9 rounded-lg bg-info-light flex items-center justify-center">
              <span class="text-info-dark font-bold text-sm">Q</span>
            </div>
          </div>
          <div class="mt-3">
            <h3 class="text-2xl font-bold text-foreground font-mono">Q {{ fmt(summary.cash.opening_gtq) }}</h3>
            <p class="text-xs text-muted mt-1">{{ summary.cash.is_open ? 'Caja abierta' : 'Sin sesión' }}</p>
          </div>
        </div>

        <!-- Comisiones del día -->
        <div class="p-6 rounded-xl bg-card shadow-sm ring-1 ring-border transition-shadow hover:shadow-md">
          <div class="flex items-center justify-between">
            <p class="text-sm font-medium text-muted">Comisiones del día</p>
            <div class="w-9 h-9 rounded-lg bg-success-light flex items-center justify-center">
              <span class="text-success-dark font-bold text-sm">%</span>
            </div>
          </div>
          <div class="mt-3">
            <h3 class="text-2xl font-bold text-foreground font-mono">Q {{ fmt(summary.commission_today) }}</h3>
            <p class="text-xs text-muted mt-1">Acumulado hoy</p>
          </div>
        </div>

        <!-- Operaciones hoy -->
        <div class="p-6 rounded-xl bg-card shadow-sm ring-1 ring-border transition-shadow hover:shadow-md">
          <div class="flex items-center justify-between">
            <p class="text-sm font-medium text-muted">Operaciones (Hoy)</p>
            <div class="w-9 h-9 rounded-lg bg-warning-light flex items-center justify-center">
              <span class="text-warning-dark font-bold text-sm">#</span>
            </div>
          </div>
          <div class="mt-3">
            <h3 class="text-2xl font-bold text-foreground">{{ summary.transactions_today }}</h3>
            <p class="text-xs text-muted mt-1">{{ summary.active_clients }} clientes activos</p>
          </div>
        </div>
      </div>

      <!-- Quick Access & Recent -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Quick Access -->
        <div class="col-span-1 p-6 rounded-xl bg-card ring-1 ring-border shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-foreground">Accesos Rápidos</h3>
          <div class="grid grid-cols-2 gap-3">
            <router-link to="/clients" class="flex flex-col items-center justify-center p-4 text-center transition-all border rounded-lg border-border bg-background hover:bg-primary-light hover:text-primary-dark hover:border-primary hover:shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              <span class="text-sm font-medium">Clientes</span>
            </router-link>
            <router-link to="/transactions" class="flex flex-col items-center justify-center p-4 text-center transition-all border rounded-lg border-border bg-background hover:bg-info-light hover:text-info-dark hover:border-info hover:shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2"><path d="M8 3L4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/></svg>
              <span class="text-sm font-medium">Transacciones</span>
            </router-link>
            <router-link to="/cash" class="flex flex-col items-center justify-center p-4 text-center transition-all border rounded-lg border-border bg-background hover:bg-warning-light hover:text-warning-dark hover:border-warning hover:shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/></svg>
              <span class="text-sm font-medium">Caja</span>
            </router-link>
            <router-link to="/reports" class="flex flex-col items-center justify-center p-4 text-center transition-all border rounded-lg border-border bg-background hover:bg-primary-light/50 hover:text-foreground hover:border-border hover:shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 18v-4"/><path d="M14 18v-6"/></svg>
              <span class="text-sm font-medium">Reportes</span>
            </router-link>
            <router-link to="/ledger/:clientId" class="flex flex-col items-center justify-center p-4 text-center transition-all border rounded-lg border-border bg-background hover:bg-slate-100 dark:hover:bg-slate-800 hover:border-slate-400 hover:shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mb-2 text-slate-500"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
              <span class="text-sm font-medium">Libro Mayor</span>
            </router-link>
          </div>
        </div>

        <!-- Recent Operations -->
        <div class="col-span-1 lg:col-span-2 p-6 rounded-xl bg-card ring-1 ring-border shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-foreground">Operaciones Recientes</h3>
          <div v-if="summary.recent_transactions.length > 0" class="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Cliente</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead class="text-right">MXN</TableHead>
                  <TableHead class="text-right">GTQ</TableHead>
                  <TableHead>Estado</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow v-for="txn in summary.recent_transactions" :key="txn.id">
                  <TableCell class="font-medium whitespace-nowrap">
                    <router-link :to="`/ledger/${txn.client_id}?from=dashboard`" class="text-primary hover:underline hover:text-primary-dark" title="Ver Libro Mayor del Cliente" v-if="txn.client_id">
                      {{ txn.client_name }}
                    </router-link>
                    <span v-else>{{ txn.client_name }}</span>
                  </TableCell>
                  <TableCell>
                    <span class="px-2 py-0.5 text-[10px] uppercase font-bold rounded-full" :class="typeClass(txn.transaction_type)">
                      {{ typeLabel(txn.transaction_type) }}
                    </span>
                  </TableCell>
                  <TableCell class="text-right font-mono">{{ fmt(txn.amount_mxn) }}</TableCell>
                  <TableCell class="text-right font-mono">{{ fmt(txn.amount_gtq) }}</TableCell>
                  <TableCell>
                    <span class="text-xs font-medium text-success">Activa</span>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </div>
          <p v-else class="text-center py-6 text-muted">No hay operaciones recientes.</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/modules/auth/stores/authStore'
import { storeToRefs } from 'pinia'
import http from '@/services/http'
import { Button } from '@/theme/components/ui/button'
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/theme/components/ui/table'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

interface DashboardSummary {
  active_clients: number
  transactions_today: number
  commission_today: string
  cash: {
    is_open: boolean
    opening_mxn: string
    opening_gtq: string
  }
  recent_transactions: Array<{
    id: string
    code: string
    client_name: string
    client_id?: string
    transaction_type: string
    amount_mxn: string
    amount_gtq: string
    commission: string
    status: string
  }>
}

const summary = ref<DashboardSummary | null>(null)
const loading = ref(true)

const fmt = (val?: string | number | null) => {
  if (val === undefined || val === null) return '0.00'
  const n = Number(val)
  if (n === 0) return '0.00'
  return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const typeLabel = (t: string) => {
  const m: Record<string, string> = {
    SELL_MXN: 'Venta MXN',
    BUY_MXN: 'Compra MXN',
    SELL_GTQ: 'Venta GTQ',
    BUY_GTQ: 'Compra GTQ',
    PAYMENT: 'Abono',
    WITHDRAWAL: 'Retiro',
  }
  return m[t] || t
}

const typeClass = (t: string) => {
  const m: Record<string, string> = {
    SELL_MXN: 'bg-info-light text-info-dark',
    BUY_MXN: 'bg-success-light text-success-dark',
    SELL_GTQ: 'bg-primary-light text-primary-dark',
    BUY_GTQ: 'bg-accent-light text-accent-dark',
    PAYMENT: 'bg-primary-light text-primary-dark',
    WITHDRAWAL: 'bg-warning-light text-warning-dark',
  }
  return m[t] || 'bg-active text-foreground'
}

onMounted(async () => {
  if (!user.value) await authStore.fetchMe()
  try {
    const { data } = await http.get('/api/v1/dashboard/summary')
    summary.value = data
  } catch (e) {
    console.error('Error loading dashboard', e)
  } finally {
    loading.value = false
  }
})
</script>
