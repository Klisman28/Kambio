<template>
  <div class="px-5 py-6">
    <div class="flex justify-between items-center mb-6">
      <div>
        <Button variant="outline" size="sm" @click="$router.push('/clients')" class="mb-2">
          &larr; Volver
        </Button>
        <h1 class="text-2xl font-bold">Detalle del Cliente</h1>
      </div>
    </div>

    <div v-if="loading" class="text-center py-10">Cargando...</div>

    <div v-else-if="client" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- Info Tarjeta -->
      <div class="bg-background border rounded-xl p-6 shadow-sm col-span-1">
        <h3 class="font-bold text-lg mb-4">{{ client.full_name }}</h3>
        <p class="text-sm text-muted-foreground mb-1">Código: <span class="font-mono text-primary">{{ client.code }}</span></p>
        <p class="text-sm text-muted-foreground mb-1">Email: {{ client.email || '—' }}</p>
        <p class="text-sm text-muted-foreground mb-4">Estado: {{ client.is_active ? 'Activo' : 'Inactivo' }}</p>
        <hr class="my-4" />
        
        <h4 class="font-semibold text-sm mb-2">Saldos Actuales</h4>
        <div class="bg-slate-50 dark:bg-slate-900 p-3 rounded-lg mb-2 flex justify-between">
          <span class="font-medium text-slate-500">MXN</span>
          <span class="font-bold font-mono">{{ formatCurrency(balance?.mxn) }}</span>
        </div>
        <div class="bg-slate-50 dark:bg-slate-900 p-3 rounded-lg flex justify-between">
          <span class="font-medium text-slate-500">GTQ</span>
          <span class="font-bold font-mono">{{ formatCurrency(balance?.gtq) }}</span>
        </div>
      </div>

      <!-- Ledger / Movimientos -->
      <div class="bg-background border rounded-xl p-6 shadow-sm col-span-1 md:col-span-2">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-lg">Libro Mayor</h3>
          <p class="text-xs text-muted-foreground">Últimos movimientos</p>
        </div>

        <Table v-if="ledger.length">
          <TableHeader>
            <TableRow>
              <TableHead>Fecha</TableHead>
              <TableHead>Divisa</TableHead>
              <TableHead>Operación</TableHead>
              <TableHead class="text-right">Monto</TableHead>
              <TableHead class="text-right">Saldo Final</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="entry in ledger" :key="entry.id">
              <TableCell class="text-xs whitespace-nowrap">{{ formatDate(entry.created_at) }}</TableCell>
              <TableCell>{{ entry.currency }}</TableCell>
              <TableCell>
                <span :class="entry.direction === 'CREDIT' ? 'text-green-600' : 'text-red-600'">
                  {{ entry.direction === 'CREDIT' ? 'Abono (+)' : 'Cargo (-)' }}
                </span>
              </TableCell>
              <TableCell class="text-right font-mono">{{ formatCurrency(entry.amount) }}</TableCell>
              <TableCell class="text-right font-mono">{{ formatCurrency(entry.balance_after) }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <p v-else class="text-center py-6 text-muted-foreground">No hay movimientos registrados.</p>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Button } from '@theme/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@theme/components/ui/table'
import http from '@/services/http'

const route = useRoute()
const clientId = route.params.id as string

const client = ref<any>(null)
const balance = ref<any>(null)
const ledger = ref<any[]>([])
const loading = ref(true)

const formatCurrency = (val: string | number) => {
  if (val === undefined || val === null) return '0.00'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

onMounted(async () => {
  try {
    const [clientRes, balRes, ledRes] = await Promise.all([
      http.get(`/api/v1/clients/${clientId}`),
      http.get(`/api/v1/clients/${clientId}/balance`),
      http.get(`/api/v1/clients/${clientId}/ledger?limit=10`)
    ])
    client.value = clientRes.data
    balance.value = balRes.data
    ledger.value = ledRes.data.entries || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>
