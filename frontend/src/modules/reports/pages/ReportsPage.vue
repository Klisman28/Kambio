<template>
  <div class="px-5 py-6 space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-foreground">Reportes</h1>
      <p class="text-sm text-muted">Centro de control y estadísticas</p>
    </div>

    <!-- Options Card -->
    <div class="bg-card border border-border rounded-xl shadow-sm p-5 space-y-4">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-end">
        <div class="flex flex-col gap-1.5 flex-1 max-w-[200px]">
          <label class="text-sm font-medium text-muted">Tipo de Reporte</label>
          <select v-model="reportType" class="h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary">
            <option value="transactions">Transacciones</option>
            <option value="cash">Cortes de Caja</option>
          </select>
        </div>
        
        <div class="flex flex-col gap-1.5 flex-1 max-w-[150px]">
          <label class="text-sm font-medium text-muted">Fecha Inicio</label>
          <input type="date" v-model="startDate" class="h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
        </div>
        
        <div class="flex flex-col gap-1.5 flex-1 max-w-[150px]">
          <label class="text-sm font-medium text-muted">Fecha Fin</label>
          <input type="date" v-model="endDate" class="h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
        </div>

        <Button @click="generateReport" :disabled="loading" class="h-10">
          {{ loading ? 'Generando...' : 'Generar' }}
        </Button>
      </div>
    </div>

    <!-- 1. Transaction Report View -->
    <div v-if="reportType === 'transactions' && transactionReport" class="space-y-6">
      
      <!-- KPIs -->
      <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
        <div class="p-4 rounded-xl bg-card border border-border shadow-sm">
          <p class="text-xs font-semibold uppercase text-muted">Operaciones</p>
          <h3 class="mt-2 text-2xl font-bold text-foreground">{{ transactionReport.summary.total_transactions }}</h3>
        </div>
        <div class="p-4 rounded-xl bg-card border border-border shadow-sm">
          <p class="text-xs font-semibold uppercase text-muted">Comisiones</p>
          <h3 class="mt-2 text-2xl font-bold text-success-dark font-mono bg-success-light px-2 rounded w-fit">Q {{ fmt(transactionReport.summary.total_commission) }}</h3>
        </div>
        <div class="p-4 rounded-xl bg-card border border-border shadow-sm">
          <p class="text-xs font-semibold uppercase text-muted">Movimiento MXN</p>
          <h3 class="mt-2 text-xl font-bold text-foreground font-mono">$ {{ fmt(transactionReport.summary.total_amount_mxn) }}</h3>
        </div>
        <div class="p-4 rounded-xl bg-card border border-border shadow-sm">
          <p class="text-xs font-semibold uppercase text-muted">Movimiento GTQ</p>
          <h3 class="mt-2 text-xl font-bold text-foreground font-mono">Q {{ fmt(transactionReport.summary.total_amount_gtq) }}</h3>
        </div>
      </div>

      <!-- Table Details -->
      <div class="bg-card border border-border rounded-xl shadow-sm overflow-hidden">
        <div class="px-5 py-4 border-b border-border flex justify-between items-center">
          <h3 class="text-base font-bold text-foreground">Detalle de Transacciones</h3>
          <Button variant="outline" size="sm" @click="exportTransactions">Exportar CSV</Button>
        </div>
        
        <div class="overflow-x-auto">
          <Table v-if="transactionReport.transactions.length > 0">
            <TableHeader>
              <TableRow>
                <TableHead>Fecha</TableHead>
                <TableHead>Código</TableHead>
                <TableHead>Cliente</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead class="text-right">MXN</TableHead>
                <TableHead class="text-right">GTQ</TableHead>
                <TableHead class="text-right">Comisión</TableHead>
                <TableHead>Estado</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="t in transactionReport.transactions" :key="t.id">
                <TableCell class="text-xs whitespace-nowrap">{{ formatDateTime(t.created_at) }}</TableCell>
                <TableCell class="font-mono text-xs">{{ t.code }}</TableCell>
                <TableCell class="text-xs">{{ clientName(t.client_id) }}</TableCell>
                <TableCell class="text-xs">{{ t.transaction_type }}</TableCell>
                <TableCell class="text-right font-mono text-xs">{{ fmt(t.amount_mxn) }}</TableCell>
                <TableCell class="text-right font-mono text-xs">{{ fmt(t.amount_gtq) }}</TableCell>
                <TableCell class="text-right font-mono text-xs">{{ fmt(t.commission) }}</TableCell>
                <TableCell class="text-xs font-bold">{{ t.status === 'ACTIVE' ? 'Activa' : 'Anulada' }}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
          <div v-else class="p-6 text-center text-muted">No hay datos en este rango de fechas.</div>
        </div>
      </div>
    </div>

    <!-- 2. Cash Report View -->
    <div v-if="reportType === 'cash' && cashReport" class="space-y-6">
      
      <!-- KPIs -->
      <div class="grid grid-cols-2 gap-4 md:grid-cols-3">
        <div class="p-4 rounded-xl bg-card border border-border shadow-sm">
          <p class="text-xs font-semibold uppercase text-muted">Cortes de Caja</p>
          <h3 class="mt-2 text-2xl font-bold text-foreground">{{ cashReport.summary.total_sessions }}</h3>
        </div>
        <div class="p-4 rounded-xl bg-card border border-border shadow-sm">
          <p class="text-xs font-semibold uppercase text-muted">Diferencias MXN (Neto)</p>
          <h3 class="mt-2 text-xl font-bold font-mono px-2 py-0.5 rounded w-fit" :class="diffClass(cashReport.summary.total_difference_mxn)">
            $ {{ fmt(cashReport.summary.total_difference_mxn) }}
          </h3>
        </div>
        <div class="p-4 rounded-xl bg-card border border-border shadow-sm">
          <p class="text-xs font-semibold uppercase text-muted">Diferencias GTQ (Neto)</p>
          <h3 class="mt-2 text-xl font-bold font-mono px-2 py-0.5 rounded w-fit" :class="diffClass(cashReport.summary.total_difference_gtq)">
            Q {{ fmt(cashReport.summary.total_difference_gtq) }}
          </h3>
        </div>
      </div>

      <!-- Table Details -->
      <div class="bg-card border border-border rounded-xl shadow-sm overflow-hidden">
        <div class="px-5 py-4 border-b border-border flex justify-between items-center">
          <h3 class="text-base font-bold text-foreground">Detalle de Cortes</h3>
          <Button variant="outline" size="sm" @click="exportCash">Exportar CSV</Button>
        </div>
        
        <div class="overflow-x-auto">
          <Table v-if="cashReport.sessions.length > 0">
            <TableHeader>
              <TableRow>
                <TableHead>Apertura</TableHead>
                <TableHead>Cierre</TableHead>
                <TableHead class="text-right">Ap. MXN</TableHead>
                <TableHead class="text-right">Ap. GTQ</TableHead>
                <TableHead class="text-right">Cie. MXN</TableHead>
                <TableHead class="text-right">Dif. MXN</TableHead>
                <TableHead class="text-right">Cie. GTQ</TableHead>
                <TableHead class="text-right">Dif. GTQ</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="s in cashReport.sessions" :key="s.id">
                <TableCell class="text-xs whitespace-nowrap">{{ formatDateTime(s.opened_at) }}</TableCell>
                <TableCell class="text-xs whitespace-nowrap">{{ s.closed_at ? formatDateTime(s.closed_at) : 'En curso' }}</TableCell>
                <TableCell class="text-right font-mono text-xs">{{ fmt(s.opening_amount_mxn) }}</TableCell>
                <TableCell class="text-right font-mono text-xs">{{ fmt(s.opening_amount_gtq) }}</TableCell>
                <TableCell class="text-right font-mono text-xs">{{ fmt(s.closing_amount_mxn) }}</TableCell>
                <TableCell class="text-right font-mono text-xs font-bold" :class="diffClassText(s.difference_mxn)">{{ fmt(s.difference_mxn) }}</TableCell>
                <TableCell class="text-right font-mono text-xs">{{ fmt(s.closing_amount_gtq) }}</TableCell>
                <TableCell class="text-right font-mono text-xs font-bold" :class="diffClassText(s.difference_gtq)">{{ fmt(s.difference_gtq) }}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
          <div v-else class="p-6 text-center text-muted">No hay cortes de caja en este rango de fechas.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useReports } from '@/modules/reports/composables/useReports'
import { useClients } from '@/modules/clients/composables/useClients'
import { Button } from '@/theme/components/ui/button'
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/theme/components/ui/table'
import { push } from 'notivue'

const { loading, transactionReport, cashReport, loadTransactionReport, loadCashReport } = useReports()
const { clients, loadClients } = useClients()

const reportType = ref<'transactions' | 'cash'>('transactions')

const today = new Date().toISOString().split('T')[0]
const firstDayOfMonth = new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0]

const startDate = ref(firstDayOfMonth)
const endDate = ref(today)

onMounted(() => {
  loadClients()
})

const clientMap = computed(() => {
  const map: Record<string, string> = {}
  clients.value.forEach(c => { map[c.id] = c.full_name })
  return map
})

const clientName = (id: string) => clientMap.value[id] || 'N/A'

const fmt = (val?: string | number | null) => {
  if (val === undefined || val === null) return '0.00'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDateTime = (d: string) => new Date(d).toLocaleString()

const diffClass = (val?: string | number | null) => {
  const n = Number(val || 0)
  if (n > 0) return 'bg-success-light text-success-dark'
  if (n < 0) return 'bg-error-light text-error-dark'
  return 'bg-primary-light text-primary-dark'
}

const diffClassText = (val?: string | number | null) => {
  const n = Number(val || 0)
  if (n > 0) return 'text-success-dark'
  if (n < 0) return 'text-error-dark'
  return 'text-muted'
}

async function generateReport() {
  if (!startDate.value || !endDate.value) {
    push.error('Debes seleccionar un rango de fechas válido')
    return
  }
  
  if (reportType.value === 'transactions') {
    await loadTransactionReport(startDate.value, endDate.value)
  } else {
    await loadCashReport(startDate.value, endDate.value)
  }
}

function triggerDownload(csvContent: string, fileName: string) {
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', fileName)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

function exportTransactions() {
  if (!transactionReport.value || !transactionReport.value.transactions.length) return
  
  const headers = ['Fecha', 'Codigo', 'Cliente', 'Tipo', 'MXN', 'GTQ', 'Comision', 'Estado']
  const rows = transactionReport.value.transactions.map(t => [
    formatDateTime(t.created_at),
    t.code,
    `"${clientName(t.client_id)}"`,
    t.transaction_type,
    t.amount_mxn,
    t.amount_gtq,
    t.commission,
    t.status
  ])
  
  const csvContent = [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
  triggerDownload(csvContent, `reporte_transacciones_${startDate.value}_${endDate.value}.csv`)
}

function exportCash() {
  if (!cashReport.value || !cashReport.value.sessions.length) return
  
  const headers = ['Apertura', 'Cierre', 'Ap. MXN', 'Ap. GTQ', 'Cie. MXN', 'Dif. MXN', 'Cie. GTQ', 'Dif. GTQ']
  const rows = cashReport.value.sessions.map(s => [
    formatDateTime(s.opened_at),
    s.closed_at ? formatDateTime(s.closed_at) : 'En curso',
    s.opening_amount_mxn,
    s.opening_amount_gtq,
    s.closing_amount_mxn || '0',
    s.difference_mxn || '0',
    s.closing_amount_gtq || '0',
    s.difference_gtq || '0'
  ])
  
  const csvContent = [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
  triggerDownload(csvContent, `resumen_caja_${startDate.value}_${endDate.value}.csv`)
}
</script>
