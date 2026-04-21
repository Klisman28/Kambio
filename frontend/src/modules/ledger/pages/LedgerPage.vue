<template>
  <div class="px-5 py-5 space-y-5 max-w-[1400px] mx-auto">

    <!-- Header: limpio, plano, sin decoración -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button v-if="navigationOrigin" @click="goBack" class="text-muted hover:text-foreground transition-colors" title="Volver">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
        </button>
        <div>
          <h1 class="text-lg font-semibold text-foreground leading-tight">
            Libro Mayor<span v-if="selectedClientName" class="text-muted font-normal"> · {{ selectedClientName }}</span>
          </h1>
          <p class="text-xs text-muted mt-0.5">Estado de cuenta y movimientos contables</p>
        </div>
      </div>
      <button v-if="selectedClientId && enrichedRows.length" @click="exportCSV"
        class="text-xs text-muted hover:text-foreground border border-border rounded-md px-3 py-1.5 transition-colors flex items-center gap-1.5">
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
        CSV
      </button>
    </div>

    <!-- Filtros: banda compacta horizontal -->
    <div class="flex flex-wrap items-end gap-3 py-3 px-4 bg-card border border-border rounded-lg">
      <div class="flex flex-col gap-1 min-w-[200px] flex-1">
        <label class="text-[11px] font-medium text-muted uppercase tracking-wide">Cliente</label>
        <select v-model="selectedClientId" class="h-9 px-2.5 text-sm bg-background border border-border rounded-md text-foreground outline-none focus:border-primary transition-colors">
          <option value="" disabled>Seleccionar...</option>
          <option v-for="c in clientsList" :key="c.id" :value="c.id">{{ c.full_name }} ({{ c.code }})</option>
        </select>
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-[11px] font-medium text-muted uppercase tracking-wide">Desde</label>
        <input type="date" v-model="filterDateFrom" :disabled="!selectedClientId || loading"
          class="h-9 px-2 text-xs bg-background border border-border rounded-md text-foreground outline-none focus:border-primary disabled:opacity-40 w-[130px]" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-[11px] font-medium text-muted uppercase tracking-wide">Hasta</label>
        <input type="date" v-model="filterDateTo" :disabled="!selectedClientId || loading"
          class="h-9 px-2 text-xs bg-background border border-border rounded-md text-foreground outline-none focus:border-primary disabled:opacity-40 w-[130px]" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-[11px] font-medium text-muted uppercase tracking-wide">Divisa</label>
        <select v-model="filterCurrency" :disabled="!selectedClientId || loading"
          class="h-9 px-2.5 text-xs bg-background border border-border rounded-md text-foreground outline-none focus:border-primary disabled:opacity-40 w-[100px]">
          <option value="">Todas</option>
          <option value="MXN">MXN</option>
          <option value="GTQ">GTQ</option>
        </select>
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-[11px] font-medium text-muted uppercase tracking-wide">Tipo</label>
        <select v-model="filterType" :disabled="!selectedClientId || loading"
          class="h-9 px-2.5 text-xs bg-background border border-border rounded-md text-foreground outline-none focus:border-primary disabled:opacity-40 w-[140px]">
          <option value="">Todos</option>
          <option value="FX">Cambio (FX)</option>
          <option value="PAYMENT">Abonos</option>
          <option value="WITHDRAWAL">Retiros</option>
        </select>
      </div>

      <!-- Tasa referencial opcional -->
      <div class="flex flex-col gap-1" title="MXN por 1 GTQ. Solo para equivalencia visual, no afecta saldos.">
        <label class="text-[11px] font-medium text-muted uppercase tracking-wide flex items-center gap-1">
          Tasa ref.
          <span class="text-[9px] bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-400 px-1 py-0.5 rounded">ref.</span>
        </label>
        <input type="number" v-model="referenceRate" :disabled="!selectedClientId || loading"
          step="0.01" min="0" placeholder="MXN/GTQ"
          class="h-9 px-2 text-xs bg-background border border-border rounded-md text-foreground outline-none focus:border-primary disabled:opacity-40 w-[100px]" />
      </div>

      <Button @click="fetchLedgerData" :disabled="!selectedClientId || loading" size="sm"
        class="h-9 px-4 bg-foreground text-background hover:bg-foreground/90 text-xs font-medium">
        {{ loading ? 'Cargando...' : 'Consultar' }}
      </Button>
    </div>

    <!-- Empty State: sin cliente -->
    <div v-if="!selectedClientId" class="py-16 flex flex-col items-center justify-center text-center">
      <div class="w-10 h-10 rounded-full bg-muted/10 flex items-center justify-center mb-3">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-muted"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      </div>
      <p class="text-sm font-medium text-foreground">Selecciona un cliente</p>
      <p class="text-xs text-muted mt-1 max-w-xs">Elige un cliente del selector para consultar su historial contable.</p>
    </div>

    <!-- Loading -->
    <div v-else-if="loading" class="py-16 text-center flex flex-col items-center justify-center">
      <div class="w-6 h-6 border-2 border-foreground/20 border-t-foreground rounded-full animate-spin mb-3"></div>
      <p class="text-xs text-muted">Cargando libro mayor...</p>
    </div>

    <!-- Contenido principal -->
    <template v-else-if="normalizedBalance">

      <!-- Posición financiera --->
      <div class="flex flex-col sm:flex-row gap-3">
        <!-- MXN -->
        <div class="flex-1 bg-card border border-border rounded-lg px-5 py-4">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] font-medium text-muted uppercase tracking-wide">Posición MXN</span>
            <span class="text-[10px] font-mono text-muted">MXN</span>
          </div>
          <!-- Frase clara -->
          <p class="text-xs font-semibold mb-2"
            :class="positionColorClass(normalizedBalance.mxn.position)">
            {{ normalizedBalance.mxn.display_label }}
          </p>
          <p class="text-2xl font-semibold font-mono tracking-tight"
            :class="positionColorClass(normalizedBalance.mxn.position)">
            $ {{ fmtAmount(normalizedBalance.mxn.absolute_balance) }}
          </p>
          <p v-if="normalizedBalance.equivalent_in_gtq" class="text-[10px] text-muted mt-1.5 flex items-center gap-1">
            <span class="bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-400 px-1 py-0.5 rounded text-[9px] font-medium">ref.</span>
            ≈ Q {{ fmtAmount(normalizedBalance.equivalent_in_gtq) }} @ {{ normalizedBalance.reference_exchange_rate }}
          </p>
        </div>
        <!-- GTQ -->
        <div class="flex-1 bg-card border border-border rounded-lg px-5 py-4">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] font-medium text-muted uppercase tracking-wide">Posición GTQ</span>
            <span class="text-[10px] font-mono text-muted">GTQ</span>
          </div>
          <!-- Frase clara -->
          <p class="text-xs font-semibold mb-2"
            :class="positionColorClass(normalizedBalance.gtq.position)">
            {{ normalizedBalance.gtq.display_label }}
          </p>
          <p class="text-2xl font-semibold font-mono tracking-tight"
            :class="positionColorClass(normalizedBalance.gtq.position)">
            Q {{ fmtAmount(normalizedBalance.gtq.absolute_balance) }}
          </p>
          <p v-if="normalizedBalance.equivalent_in_mxn" class="text-[10px] text-muted mt-1.5 flex items-center gap-1">
            <span class="bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-400 px-1 py-0.5 rounded text-[9px] font-medium">ref.</span>
            ≈ $ {{ fmtAmount(normalizedBalance.equivalent_in_mxn) }} @ {{ normalizedBalance.reference_exchange_rate }}
          </p>
        </div>
        <!-- Rentabilidad -->
        <div class="flex-1 bg-card border border-border rounded-lg px-5 py-4">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] font-medium text-muted uppercase tracking-wide">¿Estoy ganando?</span>
            <span class="text-[10px] font-medium px-1.5 py-0.5 rounded"
              :class="clientTxns.length > 0 ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'">
              {{ clientTxns.length }} ops.
            </span>
          </div>
          <p class="text-xs font-semibold mb-2 text-emerald-600 dark:text-emerald-400">
            {{ totalCommission > 0 ? 'Comisiones cobradas' : 'Sin comisiones registradas' }}
          </p>
          <p class="text-2xl font-semibold font-mono tracking-tight"
            :class="totalCommission > 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-muted'">
            $ {{ fmtAmount(totalCommission) }}
          </p>
          <p class="text-[10px] text-muted mt-1.5">
            Volumen: $ {{ fmtAmount(totalVolumeMxn) }} / Q {{ fmtAmount(totalVolumeGtq) }}
          </p>
        </div>
      </div>

      <!-- DEBUG TEMPORAL — eliminar cuando se confirme el balance -->
      <details class="text-[10px] font-mono bg-slate-50 dark:bg-slate-900 border border-dashed border-slate-300 rounded p-2">
        <summary class="cursor-pointer text-muted font-sans text-xs">🔍 Debug balance (expandir)</summary>
        <pre class="mt-2 overflow-auto text-slate-600 dark:text-slate-400 text-[9px]">{{ JSON.stringify(balance, null, 2) }}</pre>
      </details>

      <!-- Aviso enrich error -->
      <div v-if="enrichError" class="text-xs text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 rounded-md px-3 py-2">
        Algunos detalles extendidos no pudieron cargarse. Se muestra la información contable base.
      </div>

      <!-- Tabla principal -->
      <div class="bg-card border border-border rounded-lg overflow-hidden">
        <div class="px-4 py-3 border-b border-border flex items-center justify-between">
          <span class="text-sm font-medium text-foreground">Movimientos</span>
          <span class="text-[11px] text-muted">{{ enrichedRows.length }} registros</span>
        </div>

        <div class="overflow-x-auto">
          <Table v-if="enrichedRows.length > 0">
            <TableHeader>
              <TableRow class="bg-muted/5 border-b border-border">
                <TableHead class="text-[11px] font-medium uppercase tracking-wide text-muted w-[120px] py-2.5">Fecha</TableHead>
                <TableHead class="text-[11px] font-medium uppercase tracking-wide text-muted py-2.5">Referencia</TableHead>
                <TableHead class="text-[11px] font-medium uppercase tracking-wide text-muted py-2.5">Operación</TableHead>
                <TableHead class="text-[11px] font-medium uppercase tracking-wide text-muted text-center py-2.5 w-[60px]">Divisa</TableHead>
                <TableHead class="text-[11px] font-medium uppercase tracking-wide text-muted text-right py-2.5 w-[120px]">Monto</TableHead>
                <TableHead class="text-[11px] font-medium uppercase tracking-wide text-muted text-right py-2.5 w-[130px]">Saldo</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="item in enrichedRows" :key="item.entry_id"
                class="border-b border-border/50 hover:bg-muted/5 transition-colors">
                <!-- Fecha -->
                <TableCell class="text-xs text-muted whitespace-nowrap py-2.5 tabular-nums">
                  {{ formatDate(item.created_at) }}
                </TableCell>

                <!-- Referencia -->
                <TableCell class="py-2.5">
                  <span class="text-xs font-mono text-foreground/70">
                    {{ item.transaction_code || item.transaction_id.split('-')[0] }}
                  </span>
                </TableCell>

                <!-- Operación -->
                <TableCell class="py-2.5">
                  <div class="flex items-center gap-2">
                    <span class="w-1.5 h-1.5 rounded-full flex-shrink-0"
                      :class="item.direction === 'CREDIT' ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                    <span class="text-xs text-foreground">{{ typeLabel(item.transaction_type) }}</span>
                  </div>
                  <p v-if="item.notes" class="text-[10px] text-muted mt-0.5 ml-3.5 truncate max-w-[180px]" :title="item.notes">{{ item.notes }}</p>
                </TableCell>

                <!-- Divisa -->
                <TableCell class="text-center py-2.5">
                  <span class="text-[10px] font-mono font-medium text-muted">{{ item.currency }}</span>
                </TableCell>

                <!-- Monto -->
                <TableCell class="text-right font-mono text-xs tabular-nums py-2.5"
                  :class="item.direction === 'CREDIT' ? 'text-emerald-600 dark:text-emerald-400' : 'text-foreground'">
                  {{ item.direction === 'CREDIT' ? '+' : '−' }}{{ fmt(item.amount) }}
                </TableCell>

                <!-- Saldo Acumulado -->
                <TableCell class="text-right font-mono text-xs font-medium tabular-nums py-2.5"
                  :class="Number(item.balance_after) < 0 ? 'text-red-600 dark:text-red-400' : 'text-foreground'">
                  {{ fmt(item.balance_after) }}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>

          <!-- Sin resultados -->
          <div v-else class="py-12 text-center">
            <p class="text-sm text-muted">Sin movimientos para los filtros seleccionados.</p>
          </div>
        </div>
      </div>

      <!-- Link al perfil del cliente -->
      <div v-if="selectedClientId" class="flex justify-end">
        <router-link :to="{ name: 'client-detail', params: { id: selectedClientId }}"
          class="text-[11px] text-muted hover:text-primary transition-colors">
          Ver perfil del cliente →
        </router-link>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useClients } from '@/modules/clients/composables/useClients'
import http from '@/services/http'
import { Button } from '@/theme/components/ui/button'
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/theme/components/ui/table'
import { useRoute, useRouter } from 'vue-router'
import { push } from 'notivue'
import type { BalanceOut } from '@/types/ledger'
import { positionColorClass, positionBadgeClass, fmtAmount } from '@/types/ledger'

const { clients: clientsList, loadClients } = useClients()
const route = useRoute()
const router = useRouter()

const selectedClientId = ref((route.params.clientId as string) !== ':clientId' ? route.params.clientId as string : '')
const loading = ref(false)
const enrichError = ref(false)

const selectedClientName = computed(() => {
  const c = clientsList.value.find(client => client.id === selectedClientId.value)
  return c ? c.full_name : ''
})

const navigationOrigin = computed(() => route.query.from as string)
const navigationOriginText = computed(() => {
  if (navigationOrigin.value === 'clients') return 'Clientes'
  if (navigationOrigin.value === 'dashboard') return 'Inicio'
  if (navigationOrigin.value === 'transactions') return 'Transacciones'
  return 'Atrás'
})

const goBack = () => {
  if (navigationOrigin.value) {
    router.push(`/${navigationOrigin.value === 'dashboard' ? '' : navigationOrigin.value}`)
  } else {
    router.push('/')
  }
}

// Estructura del nuevo contrato BalanceOut (o antiguo si el backend no se reinició)
const balance = ref<any | null>(null)
const rawLedgerEntries = ref<any[]>([])
const clientTxns = ref<any[]>([])  // transacciones del cliente para rentabilidad

const filterCurrency = ref('')
const filterType = ref('')
const filterDateFrom = ref('')
const filterDateTo = ref('')
const referenceRate = ref<string>('')  // tasa de referencia MXN por 1 GTQ (opcional)

// ── Normalización del balance (soporta formato viejo y nuevo) ─────────────────
// Formato viejo: { mxn: "363.00", gtq: "-1583.00" }
// Formato nuevo: { mxn: { raw_balance, absolute_balance, position, display_label }, gtq: {...} }
import type { CurrencyBalance } from '@/types/ledger'

function makeBalanceFromNumber(raw: number): CurrencyBalance {
  if (raw > 0) return { raw_balance: raw, absolute_balance: raw, position: 'CLIENT_OWES', display_label: 'El cliente debe' }
  if (raw < 0) return { raw_balance: raw, absolute_balance: Math.abs(raw), position: 'COMPANY_OWES', display_label: 'A favor del cliente' }
  return { raw_balance: 0, absolute_balance: 0, position: 'SETTLED', display_label: 'Saldado' }
}

const normalizedBalance = computed<BalanceOut | null>(() => {
  if (!balance.value) return null
  const b = balance.value

  // Formato nuevo: mxn es un objeto con key 'position'
  if (b.mxn && typeof b.mxn === 'object' && 'position' in b.mxn) {
    return b as BalanceOut
  }

  // Formato antiguo: mxn/gtq son strings o números simples
  const rawMxn = Number(b.mxn) || 0
  const rawGtq = Number(b.gtq) || 0
  return {
    client_id: b.client_id,
    mxn: makeBalanceFromNumber(rawMxn),
    gtq: makeBalanceFromNumber(rawGtq),
    equivalent_in_mxn: null,
    equivalent_in_gtq: null,
    reference_exchange_rate: null,
  } as BalanceOut
})

// ── Rentabilidad ─────────────────────────────────────────────────────────────
const totalCommission = computed(() =>
  clientTxns.value
    .filter(t => t.status === 'ACTIVE')
    .reduce((sum: number, t: any) => sum + Number(t.commission || 0), 0)
)
const totalVolumeMxn = computed(() =>
  clientTxns.value
    .filter(t => t.status === 'ACTIVE')
    .reduce((sum: number, t: any) => sum + Number(t.amount_mxn || 0), 0)
)
const totalVolumeGtq = computed(() =>
  clientTxns.value
    .filter(t => t.status === 'ACTIVE')
    .reduce((sum: number, t: any) => sum + Number(t.amount_gtq || 0), 0)
)

onMounted(async () => {
  await loadClients()
  if (selectedClientId.value && selectedClientId.value !== ':clientId') {
    await fetchLedgerData()
  }
})

watch(selectedClientId, (newVal) => {
  if (newVal) {
    if (route.name === 'ledger') {
      router.replace({ params: { clientId: newVal }, query: route.query })
    } else {
      router.push({ name: 'ledger', params: { clientId: newVal } })
    }
  }
})

// Reacting to filters: optionally save into query string
watch([filterCurrency, filterType, filterDateFrom, filterDateTo], () => {
  if (selectedClientId.value) {
    router.replace({ 
      query: { 
        currency: filterCurrency.value || undefined, 
        type: filterType.value || undefined,
        from: filterDateFrom.value || undefined,
        to: filterDateTo.value || undefined
      } 
    })
    fetchLedgerData()
  }
})

// Initialize filters from query
onMounted(() => {
  if (route.query.currency) filterCurrency.value = route.query.currency as string
  if (route.query.type) filterType.value = route.query.type as string
  if (route.query.from) filterDateFrom.value = route.query.from as string
  if (route.query.to) filterDateTo.value = route.query.to as string
})

async function fetchLedgerData() {
  if (!selectedClientId.value) return
  loading.value = true
  enrichError.value = false
  console.debug('[Ledger] fetching for client_id:', selectedClientId.value)
  try {
    const url = new URL(`/api/v1/clients/${selectedClientId.value}/ledger`, window.location.origin)
    url.searchParams.append('limit', '200')
    if (filterCurrency.value) url.searchParams.append('currency', filterCurrency.value)
    if (filterDateFrom.value) url.searchParams.append('date_from', filterDateFrom.value)
    if (filterDateTo.value) url.searchParams.append('date_to', filterDateTo.value)

    // URL del balance — siempre sin filtro de fechas (saldo total del cliente)
    const balUrl = new URL(`/api/v1/clients/${selectedClientId.value}/balance`, window.location.origin)
    if (referenceRate.value && Number(referenceRate.value) > 0) {
      balUrl.searchParams.append('reference_exchange_rate', referenceRate.value)
    }

    // 3 fetches en paralelo: ledger entries, balance official, transacciones
    const [ledgerRes, balRes, txnRes] = await Promise.all([
      http.get(url.pathname + url.search),
      http.get(balUrl.pathname + balUrl.search),
      http.get(`/api/v1/transactions?client_id=${selectedClientId.value}&limit=200`)
    ])

    balance.value = balRes.data || null
    console.debug('[Ledger] balance from /balance endpoint:', JSON.stringify(balRes.data))
    rawLedgerEntries.value = ledgerRes.data.entries
    clientTxns.value = txnRes.data || []
  } catch (e) {
    console.error('Error fetching ledger data', e)
    push.error('No se pudo cargar la contabilidad del cliente.')
    balance.value = null
    rawLedgerEntries.value = []
  } finally {
    loading.value = false
  }
}

// Data Processing (Only UI level filters for type remain, currency/dates handled by Backend)
const enrichedRows = computed(() => {
  let rows = rawLedgerEntries.value.map(entry => ({
    entry_id: entry.id,
    created_at: entry.created_at,
    transaction_id: entry.transaction_id,
    currency: entry.currency,
    direction: entry.direction, // 'CREDIT' or 'DEBIT'
    amount: entry.amount,
    balance_after: entry.balance_after,
    transaction_code: entry.transaction_code,
    transaction_type: entry.transaction_type,
    notes: entry.notes || ''
  }))
  
  if (filterType.value) {
    if (filterType.value === 'FX') {
       rows = rows.filter(r => ['BUY_MXN','SELL_MXN','BUY_GTQ','SELL_GTQ'].includes(r.transaction_type))
    } else {
       rows = rows.filter(r => r.transaction_type === filterType.value)
    }
  }

  return rows
})


function exportCSV() {
  if (enrichedRows.value.length === 0) return

  const headers = ['Fecha', 'Ref', 'Operacion', 'Divisa', 'Direccion', 'Monto', 'Saldo Post-Op', 'Notas']
  const csvRows = enrichedRows.value.map(r => [
    formatDate(r.created_at),
    r.transaction_code || r.transaction_id.split('-')[0],
    r.transaction_type || 'Desconocida',
    r.currency,
    r.direction === 'CREDIT' ? 'Abono' : 'Cargo',
    r.amount,
    r.balance_after,
    `"${r.notes || ''}"`
  ])

  const content = [headers.join(','), ...csvRows.map(e => e.join(','))].join('\n')
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', `ledger_${selectedClientId.value.slice(0, 8)}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Utility Formats
const fmt = (val?: string | number | null) => {
  if (!val || Number(val) === 0) return '0.00'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (d: string) => new Date(d).toLocaleDateString('es-GT', { 
  year: 'numeric', month: '2-digit', day: '2-digit'
})

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
</script>
