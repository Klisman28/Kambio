<template>
  <div class="px-5 py-6 space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-foreground">Inteligencia Operativa</h1>
      <p class="text-sm text-muted">Panel central de balances y analítica</p>
    </div>

    <!-- Filtros (Compacto y Moderno) -->
    <div class="bg-card border border-border rounded-xl shadow-sm p-4 sticky top-0 z-10">
      <div class="flex flex-col sm:flex-row items-center gap-4 justify-between">
        <!-- Izquierda: Switcher -->
        <div class="flex items-center gap-2 p-1 bg-background border border-border rounded-lg self-start sm:self-auto">
          <button 
            @click="reportType = 'transactions'" 
            class="px-4 py-1.5 text-sm font-medium rounded-md transition-colors"
            :class="reportType === 'transactions' ? 'bg-card shadow text-foreground' : 'text-muted hover:text-foreground'"
          >
            Transacciones
          </button>
          <button 
            @click="reportType = 'cash'" 
            class="px-4 py-1.5 text-sm font-medium rounded-md transition-colors"
            :class="reportType === 'cash' ? 'bg-card shadow text-foreground' : 'text-muted hover:text-foreground'"
          >
            Caja
          </button>
        </div>

        <!-- Derecha: Rango y Acciones -->
        <div class="flex items-center gap-3 w-full sm:w-auto">
          <div class="flex items-center gap-2 bg-background border border-border rounded-lg px-2 flex-grow sm:flex-grow-0">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-muted shrink-0"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
            <input type="date" v-model="startDate" class="h-9 w-[125px] text-sm bg-transparent border-0 text-foreground outline-none focus:ring-0" />
            <span class="text-muted text-xs font-medium">hasta</span>
            <input type="date" v-model="endDate" class="h-9 w-[125px] text-sm bg-transparent border-0 text-foreground outline-none focus:ring-0" />
          </div>
          <Button @click="generateReport" :disabled="loading" class="h-10 shrink-0">
            {{ loading ? 'Actualizando...' : 'Generar' }}
          </Button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-20 text-center flex flex-col items-center justify-center space-y-4">
      <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      <p class="text-muted font-medium">Procesando cubos de datos...</p>
    </div>

    <!-- 1. TRANSACCIONES DASHBOARD -->
    <template v-else-if="reportType === 'transactions' && transactionReport">
      <div v-if="transactionReport.transactions.length === 0" class="py-16 bg-card border border-border border-dashed rounded-xl flex flex-col items-center justify-center text-center">
        <div class="w-16 h-16 bg-primary-light/30 text-primary rounded-full flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/></svg>
        </div>
        <h3 class="text-lg font-bold">Sin actividad</h3>
        <p class="text-muted max-w-sm mt-1">No hay transacciones registradas en el período seleccionado. Prueba ampliando el rango de fechas.</p>
      </div>

      <div v-else class="space-y-6">
        <!-- KPIs Principales -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <!-- Total Ops -->
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm relative overflow-hidden group">
            <div class="absolute -right-4 -top-4 text-primary opacity-5 group-hover:opacity-10 transition-opacity">
              <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            </div>
            <p class="text-xs font-bold text-muted uppercase tracking-wider mb-2">Total Ops.</p>
            <h3 class="text-3xl font-black text-foreground">{{ transactionReport.summary.total_transactions }}</h3>
            <p class="text-[10px] text-muted mt-1">Transacciones válidas</p>
          </div>
          <!-- Comisiones -->
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm relative overflow-hidden group">
            <div class="absolute -right-4 -top-4 text-success-dark opacity-5 group-hover:opacity-10 transition-opacity">
              <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>
            </div>
            <p class="text-xs font-bold text-muted uppercase tracking-wider mb-2">Revenue / Comisiones</p>
            <div class="flex items-baseline gap-1">
              <span class="text-sm font-bold text-success-dark">Q</span>
              <h3 class="text-3xl font-black text-success-dark font-mono">{{ fmt(transactionReport.summary.total_commission) }}</h3>
            </div>
            <p class="text-[10px] text-success-dark/70 mt-1">Ganancia bruta generada</p>
          </div>
          <!-- Volumen MXN -->
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm border-b-4 border-b-[#3b82f6]">
            <p class="text-xs font-bold text-muted uppercase tracking-wider mb-2">Volumen MXN</p>
            <h3 class="text-2xl font-black text-foreground font-mono truncate" :title="`$ ${fmt(transactionReport.summary.total_amount_mxn)}`">
              $ {{ fmt(transactionReport.summary.total_amount_mxn) }}
            </h3>
            <p class="text-[10px] text-muted mt-1">Monto base movido</p>
          </div>
          <!-- Volumen GTQ -->
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm border-b-4 border-b-[#8b5cf6]">
            <p class="text-xs font-bold text-muted uppercase tracking-wider mb-2">Volumen GTQ</p>
            <h3 class="text-2xl font-black text-foreground font-mono truncate" :title="`Q ${fmt(transactionReport.summary.total_amount_gtq)}`">
              Q {{ fmt(transactionReport.summary.total_amount_gtq) }}
            </h3>
            <p class="text-[10px] text-muted mt-1">Monto equivalente movido</p>
          </div>
        </div>

        <!-- GRÁFICAS Row 1 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-card border border-border rounded-xl shadow-sm p-5">
            <h3 class="text-sm font-bold mb-4">Evolución de Transacciones Diario</h3>
            <div class="h-64">
              <VueApexCharts width="100%" height="100%" type="area" :options="txnOptionsEvolucion" :series="txnSeriesEvolucion" />
            </div>
          </div>
          <div class="bg-card border border-border rounded-xl shadow-sm p-5">
            <h3 class="text-sm font-bold mb-4">Volumen Tranzado MXN vs GTQ</h3>
            <div class="h-64">
              <VueApexCharts width="100%" height="100%" type="bar" :options="txnOptionsVolume" :series="txnSeriesVolume" />
            </div>
          </div>
        </div>

        <!-- GRÁFICAS Row 2 -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="bg-card border border-border rounded-xl shadow-sm p-5 lg:col-span-1 flex flex-col">
            <h3 class="text-sm font-bold mb-4">Distribución por Tipo (Vol)</h3>
            <div class="flex-grow flex items-center justify-center">
              <VueApexCharts width="100%" height="300" type="donut" :options="txnOptionsType" :series="txnSeriesType" />
            </div>
          </div>
          <div class="bg-card border border-border rounded-xl shadow-sm overflow-hidden lg:col-span-2 flex flex-col">
            <div class="px-5 py-4 border-b border-border flex justify-between items-center bg-muted/10">
              <h3 class="text-base font-bold text-foreground">Detalle de Transacciones</h3>
              <Button variant="outline" size="sm" @click="exportTransactions" class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
                Exportar CSV
              </Button>
            </div>
            
            <div class="overflow-y-auto flex-grow max-h-[300px]">
              <Table>
                <TableHeader class="sticky top-0 bg-card z-10 shadow-sm">
                  <TableRow>
                    <TableHead>Fecha</TableHead>
                    <TableHead>Cliente</TableHead>
                    <TableHead>Tipo</TableHead>
                    <TableHead class="text-right">MXN</TableHead>
                    <TableHead class="text-right">GTQ</TableHead>
                    <TableHead>Est.</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow v-for="t in transactionReport.transactions" :key="t.id">
                    <TableCell class="text-[11px] whitespace-nowrap text-muted">{{ formatDateTime(t.created_at) }}</TableCell>
                    <TableCell class="text-xs font-medium">{{ clientName(t.client_id) }}</TableCell>
                    <TableCell>
                      <span class="px-1.5 py-0.5 text-[9px] uppercase font-bold rounded bg-primary-light text-primary-dark">
                        {{ t.transaction_type }}
                      </span>
                    </TableCell>
                    <TableCell class="text-right font-mono text-xs">{{ fmt(t.amount_mxn) }}</TableCell>
                    <TableCell class="text-right font-mono text-xs">{{ fmt(t.amount_gtq) }}</TableCell>
                    <TableCell>
                      <div class="w-2 h-2 rounded-full" :class="t.status === 'ACTIVE' ? 'bg-success' : 'bg-error'" :title="t.status"></div>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- 2. CAJA DASHBOARD -->
    <template v-else-if="reportType === 'cash' && cashReport">
      <div v-if="cashReport.sessions.length === 0" class="py-16 bg-card border border-border border-dashed rounded-xl flex flex-col items-center justify-center text-center">
        <div class="w-16 h-16 bg-primary-light/30 text-primary rounded-full flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
        </div>
        <h3 class="text-lg font-bold">Sin cortes</h3>
        <p class="text-muted max-w-sm mt-1">No hay sesiones de caja registradas en el período seleccionado.</p>
      </div>

      <div v-else class="space-y-6">
        <!-- KPIs Caja -->
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm text-center">
            <p class="text-xs font-bold text-muted uppercase tracking-wider mb-2">Turnos / Cortes</p>
            <h3 class="text-3xl font-black text-foreground">{{ cashReport.summary.total_sessions }}</h3>
          </div>
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm text-center flex flex-col items-center">
            <p class="text-xs font-bold text-muted uppercase tracking-wider mb-2">Descuadre Neto MXN</p>
            <h3 class="text-2xl font-black font-mono px-3 py-1 rounded w-fit" :class="diffClass(cashReport.summary.total_difference_mxn)">
              $ {{ fmt(cashReport.summary.total_difference_mxn) }}
            </h3>
          </div>
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm text-center flex flex-col items-center">
            <p class="text-xs font-bold text-muted uppercase tracking-wider mb-2">Descuadre Neto GTQ</p>
            <h3 class="text-2xl font-black font-mono px-3 py-1 rounded w-fit" :class="diffClass(cashReport.summary.total_difference_gtq)">
              Q {{ fmt(cashReport.summary.total_difference_gtq) }}
            </h3>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-card border border-border rounded-xl shadow-sm p-5">
            <h3 class="text-sm font-bold mb-4">Diferencias de Efectivo por Turno</h3>
            <div class="h-64">
              <VueApexCharts width="100%" height="100%" type="bar" :options="cashOptionsDiff" :series="cashSeriesDiff" />
            </div>
          </div>
          <div class="bg-card border border-border rounded-xl shadow-sm overflow-hidden flex flex-col">
            <div class="px-5 py-4 border-b border-border flex justify-between items-center bg-muted/10">
              <h3 class="text-base font-bold text-foreground">Registro de Sesiones</h3>
              <Button variant="outline" size="sm" @click="exportCash" class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
                Exportar CSV
              </Button>
            </div>
            
            <div class="overflow-y-auto flex-grow max-h-[300px]">
              <Table>
                <TableHeader class="sticky top-0 bg-card z-10 shadow-sm">
                  <TableRow>
                    <TableHead>Fecha</TableHead>
                    <TableHead class="text-right">Ap. MXN</TableHead>
                    <TableHead class="text-right">Ap. GTQ</TableHead>
                    <TableHead class="text-right">Dif. MXN</TableHead>
                    <TableHead class="text-right">Dif. GTQ</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow v-for="s in cashReport.sessions" :key="s.id">
                    <TableCell class="text-[11px] whitespace-nowrap text-muted font-medium">{{ formatD(s.opened_at) }}</TableCell>
                    <TableCell class="text-right font-mono text-xs">{{ fmt(s.opening_amount_mxn) }}</TableCell>
                    <TableCell class="text-right font-mono text-xs">{{ fmt(s.opening_amount_gtq) }}</TableCell>
                    <TableCell class="text-right font-mono text-xs font-bold" :class="diffClassText(s.difference_mxn)">{{ fmt(s.difference_mxn) }}</TableCell>
                    <TableCell class="text-right font-mono text-xs font-bold" :class="diffClassText(s.difference_gtq)">{{ fmt(s.difference_gtq) }}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import VueApexCharts from 'vue3-apexcharts'
import { useReports } from '@/modules/reports/composables/useReports'
import { useClients } from '@/modules/clients/composables/useClients'
import { Button } from '@/theme/components/ui/button'
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/theme/components/ui/table'
import { push } from 'notivue'

const { loading, transactionReport, transactionAnalytics, cashReport, loadTransactionReport, loadCashReport } = useReports()
const { clients, loadClients } = useClients()

const reportType = ref<'transactions' | 'cash'>('transactions')

const today = new Date()
const firstDay = new Date(today.getFullYear(), today.getMonth(), 1)
// Ajuste timezone offset local a ISO
const toIsoLocal = (d: Date) => {
  const dt = new Date(d.getTime() - (d.getTimezoneOffset() * 60000))
  return dt.toISOString().split('T')[0]
}

const startDate = ref(toIsoLocal(firstDay))
const endDate = ref(toIsoLocal(today))

// Generar inicial
onMounted(async () => {
  await loadClients()
  await generateReport()
})

watch(reportType, () => generateReport())

// ========================
// CHART COMPUTEDS (TXN)
// ========================

// Grafica 1: Line Area (Ops per day)
const txnSeriesEvolucion = computed(() => {
  if (!transactionAnalytics.value) return []
  const data = transactionAnalytics.value.daily_series.map(d => ({ x: d.date, y: d.count }))
  return [{ name: 'Operaciones exitosas', data }]
})

const txnOptionsEvolucion = computed(() => ({
  chart: { type: 'area', fontFamily: 'inherit', toolbar: { show: false }, zoom: { enabled: false } },
  stroke: { curve: 'smooth', width: 2 },
  colors: ['#22c55e'], 
  fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.4, opacityTo: 0.0, stops: [0, 100] } },
  xaxis: { type: 'datetime', labels: { style: { cssClass: 'text-xs text-muted font-sans' } } },
  yaxis: { labels: { style: { cssClass: 'text-xs text-muted font-sans' } } },
  dataLabels: { enabled: false },
  grid: { borderColor: 'rgba(150, 150, 150, 0.1)' }
}))

// Grafica 2: Bar (Vol MXN vs GTQ)
const txnSeriesVolume = computed(() => {
  if (!transactionAnalytics.value) return []
  return [
    { name: 'MXN ($)', data: transactionAnalytics.value.daily_series.map(d => ({ x: d.date, y: Number(d.amount_mxn) })) },
    { name: 'GTQ (Q)', data: transactionAnalytics.value.daily_series.map(d => ({ x: d.date, y: Number(d.amount_gtq) })) }
  ]
})

const txnOptionsVolume = computed(() => ({
  chart: { type: 'bar', fontFamily: 'inherit', toolbar: { show: false } },
  colors: ['#3b82f6', '#8b5cf6'],
  xaxis: { type: 'category', labels: { style: { cssClass: 'text-xs text-muted font-sans' }, hideOverlappingLabels: true } },
  yaxis: { labels: { style: { cssClass: 'text-xs text-muted font-sans' } } },
  dataLabels: { enabled: false },
  plotOptions: { bar: { borderRadius: 4, columnWidth: '60%' } },
  legend: { position: 'top', horizontalAlign: 'right' },
  grid: { borderColor: 'rgba(150, 150, 150, 0.1)' }
}))

// Grafica 3: Donut (Distribution)
const txnSeriesType = computed(() => {
  if (!transactionAnalytics.value) return []
  return transactionAnalytics.value.type_distribution.map(td => td.count)
})

const txnOptionsType = computed(() => {
  if (!transactionAnalytics.value) return {}
  const labels = transactionAnalytics.value.type_distribution.map(td => typeLabel(td.transaction_type))
  return {
    labels,
    chart: { type: 'donut', fontFamily: 'inherit' },
    colors: ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#14b8a6'],
    dataLabels: { enabled: false },
    legend: { position: 'bottom', labels: { colors: 'inherit' } },
    plotOptions: { pie: { donut: { size: '75%' } } },
    stroke: { width: 0 }
  }
})

// ========================
// CHART COMPUTEDS (CASH)
// ========================

// Bar chart diferencias
const cashSeriesDiff = computed(() => {
  if (!cashReport.value) return []
  return [
    { name: 'Dif. MXN', data: cashReport.value.sessions.map((s, i) => ({ x: `T#${s.id.split('-')[0].slice(0,4)}`, y: Number(s.difference_mxn || 0) })) },
    { name: 'Dif. GTQ', data: cashReport.value.sessions.map((s, i) => ({ x: `T#${s.id.split('-')[0].slice(0,4)}`, y: Number(s.difference_gtq || 0) })) }
  ]
})

const cashOptionsDiff = computed(() => ({
  chart: { type: 'bar', fontFamily: 'inherit', toolbar: { show: false } },
  colors: ['#22c55e', '#f43f5e'], // green for one, rose for other (it's mixed pos/neg)
  xaxis: { type: 'category', labels: { style: { cssClass: 'text-xs text-muted font-sans' } } },
  yaxis: { labels: { style: { cssClass: 'text-xs text-muted font-sans' } } },
  dataLabels: { enabled: false },
  plotOptions: { bar: { borderRadius: 4, columnWidth: '50%', colors: { ranges: [{ from: -100000, to: -0.01, color: '#ef4444' }] } } },
  legend: { position: 'top', horizontalAlign: 'right' },
  grid: { borderColor: 'rgba(150, 150, 150, 0.1)' }
}))

// ========================
// UTILS & METHODS
// ========================

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

const formatDateTime = (d: string) => new Date(d).toLocaleString('es-ES', { day: '2-digit', month: 'short', hour:'2-digit', minute:'2-digit' })
const formatD = (d: string) => new Date(d).toLocaleString('es-ES', { day: '2-digit', month: 'short' })

const diffClass = (val?: string | number | null) => {
  const n = Number(val || 0)
  if (n > 0) return 'bg-success-light text-success-dark border-success'
  if (n < 0) return 'bg-error-light text-error-dark border-error'
  return 'bg-primary-light text-primary-dark border-primary'
}

const diffClassText = (val?: string | number | null) => {
  const n = Number(val || 0)
  if (n > 0) return 'text-success-dark'
  if (n < 0) return 'text-error-dark'
  return 'text-muted'
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

async function generateReport() {
  if (!startDate.value || !endDate.value) {
    push.error('Rango de fechas inválido')
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
