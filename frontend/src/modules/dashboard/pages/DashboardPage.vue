<template>
  <div class="py-6 space-y-8">
    <!-- Header -->
    <div class="flex flex-col gap-2 md:items-center md:flex-row md:justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-foreground">Dashboard</h1>
        <p class="text-muted">Bienvenido de vuelta, {{ user?.full_name }} — Resumen General</p>
      </div>
      <div>
        <button class="px-4 py-2 font-medium text-white transition-colors rounded-lg shadow-sm bg-primary hover:bg-primary-dark">
          + Nueva Transacción
        </button>
      </div>
    </div>

    <!-- Stats Row -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
      <div class="p-6 transition-shadow border-none rounded-xl bg-card shadow-sm ring-1 ring-border">
        <div class="flex items-center justify-between">
          <p class="text-sm font-medium text-muted">Saldo GTQ (Caja)</p>
        </div>
        <div class="mt-4">
          <h3 class="text-2xl font-bold text-foreground">Q 45,230.00</h3>
        </div>
      </div>

      <div class="p-6 transition-shadow border-none rounded-xl bg-card shadow-sm ring-1 ring-border">
        <div class="flex items-center justify-between">
          <p class="text-sm font-medium text-muted">Saldo MXN (Caja)</p>
        </div>
        <div class="mt-4">
          <h3 class="text-2xl font-bold text-foreground">$ 120,400.00</h3>
        </div>
      </div>

      <div class="p-6 transition-shadow border-none rounded-xl bg-card shadow-sm ring-1 ring-border">
        <div class="flex items-center justify-between">
          <p class="text-sm font-medium text-muted">Comisiones del día</p>
        </div>
        <div class="mt-4">
          <h3 class="text-2xl font-bold text-foreground">Q 850.00</h3>
        </div>
      </div>

      <div class="p-6 transition-shadow border-none rounded-xl bg-card shadow-sm ring-1 ring-border">
        <div class="flex items-center justify-between">
          <p class="text-sm font-medium text-muted">Operaciones (Hoy)</p>
        </div>
        <div class="mt-4">
          <h3 class="text-2xl font-bold text-foreground">12</h3>
        </div>
      </div>
    </div>

    <!-- Quick Access & Recent Actions -->
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
      
      <!-- Quick Access Modules -->
      <div class="col-span-1 p-6 border-none rounded-xl bg-card ring-1 ring-border shadow-sm">
        <h3 class="mb-4 text-lg font-semibold text-foreground">Accesos Rápidos</h3>
        <div class="grid grid-cols-2 gap-4">
          <router-link to="/clients" class="flex flex-col items-center justify-center p-4 text-center transition-colors border rounded-lg border-border bg-background hover:bg-primary-light hover:text-primary-dark hover:border-primary">
            <span class="font-medium">Clientes</span>
          </router-link>
          <router-link to="/transactions" class="flex flex-col items-center justify-center p-4 text-center transition-colors border rounded-lg border-border bg-background hover:bg-info-light hover:text-info-dark hover:border-info">
            <span class="font-medium">Transacciones</span>
          </router-link>
          <router-link to="/cash" class="flex flex-col items-center justify-center p-4 text-center transition-colors border rounded-lg border-border bg-background hover:bg-warning-light hover:text-warning-dark hover:border-warning">
            <span class="font-medium">Caja</span>
          </router-link>
          <router-link to="/reports" class="flex flex-col items-center justify-center p-4 text-center transition-colors border rounded-lg border-border bg-background hover:bg-secondary-light hover:text-secondary-dark hover:border-secondary">
            <span class="font-medium">Reportes</span>
          </router-link>
        </div>
      </div>

      <!-- Recent Operations Mock -->
      <div class="col-span-1 lg:col-span-2 p-6 border-none rounded-xl bg-card ring-1 ring-border shadow-sm">
        <h3 class="mb-4 text-lg font-semibold text-foreground">Operaciones Recientes</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-sm text-left whitespace-nowrap">
            <thead class="text-muted border-b border-border">
              <tr>
                <th class="py-3 font-medium">Cliente</th>
                <th class="py-3 font-medium">Tipo</th>
                <th class="py-3 font-medium">Monto MXN</th>
                <th class="py-3 font-medium">Monto GTQ</th>
                <th class="py-3 font-medium">Estado</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr>
                <td class="py-3 font-medium">Juan Pérez</td>
                <td class="py-3"><span class="px-2 py-1 text-xs rounded-full bg-success-light text-success-dark">Compra</span></td>
                <td class="py-3">$ 5,000.00</td>
                <td class="py-3">Q 2,150.00</td>
                <td class="py-3 text-success">Completado</td>
              </tr>
              <tr>
                <td class="py-3 font-medium">Empresa XYZ</td>
                <td class="py-3"><span class="px-2 py-1 text-xs rounded-full bg-info-light text-info-dark">Venta</span></td>
                <td class="py-3">$ 10,000.00</td>
                <td class="py-3">Q 4,400.00</td>
                <td class="py-3 text-success">Completado</td>
              </tr>
              <tr>
                <td class="py-3 font-medium">María G.</td>
                <td class="py-3"><span class="px-2 py-1 text-xs rounded-full bg-success-light text-success-dark">Compra</span></td>
                <td class="py-3">$ 2,500.00</td>
                <td class="py-3">Q 1,075.00</td>
                <td class="py-3 text-success">Completado</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/modules/auth/stores/authStore'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

onMounted(async () => {
  if (!user.value) await authStore.fetchMe()
})
</script>
