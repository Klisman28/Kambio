<template>
  <div class="px-5 py-5 space-y-5 max-w-[1400px] mx-auto">

    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button v-if="navigationOrigin" @click="goBack"
          class="w-8 h-8 rounded-lg hover:bg-hover flex items-center justify-center text-muted hover:text-foreground transition-colors" title="Volver">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
        </button>
        <div>
          <h1 class="text-lg font-semibold text-foreground leading-tight">
            Libro Mayor<span v-if="selectedClientName" class="text-muted font-normal"> · {{ selectedClientName }}</span>
          </h1>
          <p class="text-xs text-muted mt-0.5">Estado de cuenta por transacción</p>
        </div>
      </div>
      <button v-if="selectedClientId && visibleRows.length" @click="exportCSV"
        class="inline-flex items-center gap-1.5 text-xs text-muted hover:text-foreground border border-border rounded-lg px-3 py-1.5 hover:bg-hover transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
        Exportar CSV
      </button>
    </div>

    <!-- Filtros -->
    <div class="flex flex-wrap items-end gap-3 py-3 px-4 bg-card border border-border rounded-xl">
      <div class="flex flex-col gap-1 min-w-[200px] flex-1">
        <label class="text-[11px] font-semibold text-muted uppercase tracking-wide">Cliente</label>
        <select v-model="selectedClientId" class="h-9 px-2.5 text-sm bg-background border border-border rounded-lg text-foreground outline-none focus:border-primary transition-colors">
          <option value="" disabled>Seleccionar...</option>
          <option v-for="c in clientsList" :key="c.id" :value="c.id">{{ c.full_name }} ({{ c.code }})</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-[11px] font-semibold text-muted uppercase tracking-wide">Desde</label>
        <input type="date" v-model="filterDateFrom" :disabled="!selectedClientId || loading"
          class="h-9 px-2 text-xs bg-background border border-border rounded-lg text-foreground outline-none focus:border-primary disabled:opacity-40 w-[130px]" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-[11px] font-semibold text-muted uppercase tracking-wide">Hasta</label>
        <input type="date" v-model="filterDateTo" :disabled="!selectedClientId || loading"
          class="h-9 px-2 text-xs bg-background border border-border rounded-lg text-foreground outline-none focus:border-primary disabled:opacity-40 w-[130px]" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-[11px] font-semibold text-muted uppercase tracking-wide">Tipo</label>
        <select v-model="filterType" :disabled="!selectedClientId || loading"
          class="h-9 px-2.5 text-xs bg-background border border-border rounded-lg text-foreground outline-none focus:border-primary disabled:opacity-40 w-[140px]">
          <option value="">Todos</option>
          <option value="FX">Cambio (FX)</option>
          <option value="PAYMENT">Abonos</option>
          <option value="WITHDRAWAL">Retiros</option>
        </select>
      </div>
      <Button @click="fetchLedgerData" :disabled="!selectedClientId || loading" size="sm"
        class="h-9 px-4 bg-foreground text-background hover:bg-foreground/90 text-xs font-medium">
        {{ loading ? 'Cargando...' : 'Consultar' }}
      </Button>
    </div>

    <!-- Empty: sin cliente -->
    <div v-if="!selectedClientId" class="py-16 flex flex-col items-center justify-center text-center">
      <div class="w-12 h-12 rounded-2xl bg-muted/10 flex items-center justify-center mb-3">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-muted"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      </div>
      <p class="text-sm font-medium text-foreground">Selecciona un cliente</p>
      <p class="text-xs text-muted mt-1 max-w-xs">Elige un cliente del selector para consultar su estado de cuenta.</p>
    </div>

    <!-- Loading -->
    <div v-else-if="loading" class="py-16 flex flex-col items-center justify-center">
      <div class="w-6 h-6 border-2 border-foreground/20 border-t-foreground rounded-full animate-spin mb-3"></div>
      <p class="text-xs text-muted">Cargando libro mayor...</p>
    </div>

    <!-- Contenido principal -->
    <template v-else-if="ledgerData">

      <!-- ── Resumen (6 stats del backend, rango completo) ── -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">

        <!-- Egreso MXN -->
        <div class="bg-card border border-border rounded-xl px-4 py-3.5">
          <p class="text-[10px] font-semibold text-muted uppercase tracking-wide mb-1">Egreso MXN</p>
          <p class="text-base font-bold font-mono text-red-600 dark:text-red-400">
            − ${{ fmtAmount(ledgerData.summary.total_egreso_mxn) }}
          </p>
        </div>

        <!-- Ingreso MXN -->
        <div class="bg-card border border-border rounded-xl px-4 py-3.5">
          <p class="text-[10px] font-semibold text-muted uppercase tracking-wide mb-1">Ingreso MXN</p>
          <p class="text-base font-bold font-mono text-emerald-600 dark:text-emerald-400">
            + ${{ fmtAmount(ledgerData.summary.total_ingreso_mxn) }}
          </p>
        </div>

        <!-- Net MXN -->
        <div class="bg-card border-2 rounded-xl px-4 py-3.5"
          :class="netBorderClass(ledgerData.summary.net_mxn_label)">
          <p class="text-[10px] font-semibold text-muted uppercase tracking-wide mb-1">Total MXN</p>
          <p class="text-base font-bold font-mono" :class="netLabelColor(ledgerData.summary.net_mxn_label)">
            {{ Number(ledgerData.summary.net_mxn) >= 0 ? '+' : '' }}${{ fmtAmount(ledgerData.summary.net_mxn) }}
          </p>
          <p class="text-[10px] mt-0.5 font-medium" :class="netLabelColor(ledgerData.summary.net_mxn_label)">
            {{ netLabelText(ledgerData.summary.net_mxn_label) }}
          </p>
        </div>

        <!-- Egreso GTQ -->
        <div class="bg-card border border-border rounded-xl px-4 py-3.5">
          <p class="text-[10px] font-semibold text-muted uppercase tracking-wide mb-1">Egreso GTQ</p>
          <p class="text-base font-bold font-mono text-red-600 dark:text-red-400">
            − Q{{ fmtAmount(ledgerData.summary.total_egreso_gtq) }}
          </p>
        </div>

        <!-- Ingreso GTQ -->
        <div class="bg-card border border-border rounded-xl px-4 py-3.5">
          <p class="text-[10px] font-semibold text-muted uppercase tracking-wide mb-1">Ingreso GTQ</p>
          <p class="text-base font-bold font-mono text-emerald-600 dark:text-emerald-400">
            + Q{{ fmtAmount(ledgerData.summary.total_ingreso_gtq) }}
          </p>
        </div>

        <!-- Net GTQ -->
        <div class="bg-card border-2 rounded-xl px-4 py-3.5"
          :class="netBorderClass(ledgerData.summary.net_gtq_label)">
          <p class="text-[10px] font-semibold text-muted uppercase tracking-wide mb-1">Total GTQ</p>
          <p class="text-base font-bold font-mono" :class="netLabelColor(ledgerData.summary.net_gtq_label)">
            {{ Number(ledgerData.summary.net_gtq) >= 0 ? '+' : '' }}Q{{ fmtAmount(ledgerData.summary.net_gtq) }}
          </p>
          <p class="text-[10px] mt-0.5 font-medium" :class="netLabelColor(ledgerData.summary.net_gtq_label)">
            {{ netLabelText(ledgerData.summary.net_gtq_label) }}
          </p>
        </div>

      </div>

      <!-- ── Tabla agrupada ── -->
      <div class="bg-card border border-border rounded-xl overflow-hidden">
        <div class="px-4 py-3 border-b border-border flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-sm font-semibold text-foreground">Movimientos</span>
            <span class="text-[11px] text-muted bg-muted/10 px-2 py-0.5 rounded-full">
              {{ visibleRows.length }} de {{ ledgerData.total }} transacciones
            </span>
          </div>
          <!-- Leyenda -->
          <div class="hidden sm:flex items-center gap-4 text-[10px] text-muted">
            <span class="flex items-center gap-1">
              <span class="w-2.5 h-2.5 rounded-sm bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 inline-block"></span>Egreso
            </span>
            <span class="flex items-center gap-1">
              <span class="w-2.5 h-2.5 rounded-sm bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 inline-block"></span>Ingreso
            </span>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table v-if="visibleRows.length > 0" class="w-full text-xs">
            <thead>
              <tr class="bg-muted/5 border-b border-border">
                <th class="text-left text-[11px] font-semibold uppercase tracking-wide text-muted px-4 py-2.5 whitespace-nowrap w-[100px]">Fecha</th>
                <th class="text-left text-[11px] font-semibold uppercase tracking-wide text-muted px-3 py-2.5 whitespace-nowrap">Referencia</th>
                <th class="text-left text-[11px] font-semibold uppercase tracking-wide text-muted px-3 py-2.5">Operación</th>
                <th class="text-right text-[11px] font-semibold uppercase tracking-wide text-red-500/70 px-3 py-2.5 whitespace-nowrap bg-red-50/30 dark:bg-red-950/10">Egreso MXN</th>
                <th class="text-right text-[11px] font-semibold uppercase tracking-wide text-red-500/70 px-3 py-2.5 whitespace-nowrap bg-red-50/30 dark:bg-red-950/10">Egreso GTQ</th>
                <th class="text-right text-[11px] font-semibold uppercase tracking-wide text-emerald-600/70 px-3 py-2.5 whitespace-nowrap bg-emerald-50/30 dark:bg-emerald-950/10">Ingreso MXN</th>
                <th class="text-right text-[11px] font-semibold uppercase tracking-wide text-emerald-600/70 px-3 py-2.5 whitespace-nowrap bg-emerald-50/30 dark:bg-emerald-950/10">Ingreso GTQ</th>
                <th class="text-left text-[11px] font-semibold uppercase tracking-wide text-muted px-3 py-2.5 hidden md:table-cell">Notas</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in visibleRows" :key="row.transaction_id"
                class="border-b border-border/50 hover:bg-muted/5 transition-colors"
                :class="row.status !== 'ACTIVE' ? 'opacity-50' : ''">

                <!-- Fecha -->
                <td class="px-4 py-2.5 text-muted whitespace-nowrap tabular-nums text-[11px]">
                  {{ formatDate(row.date) }}
                </td>

                <!-- Referencia -->
                <td class="px-3 py-2.5">
                  <span class="font-mono text-foreground/70 text-[11px]">{{ row.reference }}</span>
                </td>

                <!-- Operación -->
                <td class="px-3 py-2.5">
                  <span class="text-foreground font-medium">{{ typeLabel(row.operation) }}</span>
                </td>

                <!-- Egreso MXN -->
                <td class="px-3 py-2.5 text-right tabular-nums bg-red-50/20 dark:bg-red-950/5">
                  <span v-if="Number(row.egreso_mxn) > 0" class="font-mono font-medium text-red-600 dark:text-red-400">
                    ${{ fmtAmount(row.egreso_mxn) }}
                  </span>
                  <span v-else class="text-muted/30">—</span>
                </td>

                <!-- Egreso GTQ -->
                <td class="px-3 py-2.5 text-right tabular-nums bg-red-50/20 dark:bg-red-950/5">
                  <span v-if="Number(row.egreso_gtq) > 0" class="font-mono font-medium text-red-600 dark:text-red-400">
                    Q{{ fmtAmount(row.egreso_gtq) }}
                  </span>
                  <span v-else class="text-muted/30">—</span>
                </td>

                <!-- Ingreso MXN -->
                <td class="px-3 py-2.5 text-right tabular-nums bg-emerald-50/20 dark:bg-emerald-950/5">
                  <span v-if="Number(row.ingreso_mxn) > 0" class="font-mono font-medium text-emerald-600 dark:text-emerald-400">
                    ${{ fmtAmount(row.ingreso_mxn) }}
                  </span>
                  <span v-else class="text-muted/30">—</span>
                </td>

                <!-- Ingreso GTQ -->
                <td class="px-3 py-2.5 text-right tabular-nums bg-emerald-50/20 dark:bg-emerald-950/5">
                  <span v-if="Number(row.ingreso_gtq) > 0" class="font-mono font-medium text-emerald-600 dark:text-emerald-400">
                    Q{{ fmtAmount(row.ingreso_gtq) }}
                  </span>
                  <span v-else class="text-muted/30">—</span>
                </td>

                <!-- Notas -->
                <td class="px-3 py-2.5 hidden md:table-cell">
                  <span v-if="row.notes" class="text-[11px] text-muted truncate max-w-[160px] block" :title="row.notes">
                    {{ row.notes }}
                  </span>
                  <span v-else class="text-muted/30">—</span>
                </td>

              </tr>

              <!-- Fila net (usa los totales del backend, no suma de filas visibles) -->
              <tr class="border-t-2 border-border bg-muted/5">
                <td class="px-4 py-2.5 text-[11px] font-bold text-muted uppercase tracking-wide" colspan="3">
                  Neto del período
                </td>
                <!-- Net MXN — ocupa las 2 cols de MXN -->
                <td class="px-3 py-2.5 text-right tabular-nums" colspan="2">
                  <span class="font-mono text-sm font-bold"
                    :class="netLabelColor(ledgerData.summary.net_mxn_label)">
                    {{ Number(ledgerData.summary.net_mxn) >= 0 ? '+' : '' }}${{ fmtAmount(ledgerData.summary.net_mxn) }}
                  </span>
                  <span class="block text-[10px] text-muted font-normal">Ingreso − Egreso MXN</span>
                </td>
                <!-- Net GTQ — ocupa las 2 cols de GTQ -->
                <td class="px-3 py-2.5 text-right tabular-nums" colspan="2">
                  <span class="font-mono text-sm font-bold"
                    :class="netLabelColor(ledgerData.summary.net_gtq_label)">
                    {{ Number(ledgerData.summary.net_gtq) >= 0 ? '+' : '' }}Q{{ fmtAmount(ledgerData.summary.net_gtq) }}
                  </span>
                  <span class="block text-[10px] text-muted font-normal">Ingreso − Egreso GTQ</span>
                </td>
                <td class="hidden md:table-cell"></td>
              </tr>
            </tbody>
          </table>

          <!-- Sin resultados -->
          <div v-else class="py-14 text-center">
            <p class="text-sm text-muted">Sin movimientos para los filtros seleccionados.</p>
          </div>
        </div>
      </div>

      <!-- Link al perfil -->
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
import { useRoute, useRouter } from 'vue-router'
import { push } from 'notivue'
import type { LedgerGroupedResponse, LedgerGroupedRow } from '@/types/ledger'
import { netLabelText, netLabelColor, netBorderClass, fmtAmount } from '@/types/ledger'

const { clients: clientsList, loadClients } = useClients()
const route = useRoute()
const router = useRouter()

const selectedClientId = ref(
  (route.params.clientId as string) !== ':clientId' ? (route.params.clientId as string) : ''
)
const loading = ref(false)

const selectedClientName = computed(() => {
  const c = clientsList.value.find(client => client.id === selectedClientId.value)
  return c ? c.full_name : ''
})

const navigationOrigin = computed(() => route.query.from as string)

const goBack = () => {
  if (navigationOrigin.value) {
    router.push(`/${navigationOrigin.value === 'dashboard' ? '' : navigationOrigin.value}`)
  } else {
    router.push('/')
  }
}

// ── State ─────────────────────────────────────────────────────────────────────
const ledgerData = ref<LedgerGroupedResponse | null>(null)

const filterType    = ref('')
const filterDateFrom = ref('')
const filterDateTo   = ref('')

// ── Filas filtradas (sólo filterType es cliente-side; fecha ya va al backend) ──
const visibleRows = computed<LedgerGroupedRow[]>(() => {
  if (!ledgerData.value) return []
  let rows = ledgerData.value.rows
  if (filterType.value) {
    const fxTypes = ['BUY_MXN', 'SELL_MXN', 'BUY_GTQ', 'SELL_GTQ']
    if (filterType.value === 'FX') {
      rows = rows.filter(r => fxTypes.includes(r.operation))
    } else {
      rows = rows.filter(r => r.operation === filterType.value)
    }
  }
  return rows
})

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  await loadClients()
  if (route.query.type)       filterType.value     = route.query.type      as string
  if (route.query.date_from)  filterDateFrom.value = route.query.date_from as string
  if (route.query.date_to)    filterDateTo.value   = route.query.date_to   as string
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

// ── Fetch — único call al nuevo endpoint agrupado ────────────────────────────
async function fetchLedgerData() {
  if (!selectedClientId.value) return
  loading.value = true
  try {
    const params: Record<string, string> = { limit: '200' }
    if (filterDateFrom.value) params.date_from = filterDateFrom.value
    if (filterDateTo.value)   params.date_to   = filterDateTo.value

    const res = await http.get<LedgerGroupedResponse>(
      `/api/v1/clients/${selectedClientId.value}/ledger-summary`,
      { params }
    )
    ledgerData.value = res.data
  } catch (e) {
    console.error('Error fetching ledger-summary', e)
    push.error('No se pudo cargar el libro mayor.')
    ledgerData.value = null
  } finally {
    loading.value = false
  }
}

// ── Export CSV ─────────────────────────────────────────────────────────────────
function exportCSV() {
  if (!visibleRows.value.length) return
  const headers = ['Fecha', 'Referencia', 'Operacion', 'Egreso MXN', 'Egreso GTQ', 'Ingreso MXN', 'Ingreso GTQ', 'Notas']
  const rows = visibleRows.value.map(r => [
    formatDate(r.date),
    r.reference,
    typeLabel(r.operation),
    Number(r.egreso_mxn)  > 0 ? Number(r.egreso_mxn).toFixed(2)  : '',
    Number(r.egreso_gtq)  > 0 ? Number(r.egreso_gtq).toFixed(2)  : '',
    Number(r.ingreso_mxn) > 0 ? Number(r.ingreso_mxn).toFixed(2) : '',
    Number(r.ingreso_gtq) > 0 ? Number(r.ingreso_gtq).toFixed(2) : '',
    `"${r.notes || ''}"`,
  ])
  const content = [headers.join(','), ...rows.map(r => r.join(','))].join('\n')
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', `libro_mayor_${selectedClientId.value.slice(0, 8)}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// ── Helpers ───────────────────────────────────────────────────────────────────
const formatDate = (d: string) =>
  new Date(d).toLocaleDateString('es-GT', { year: 'numeric', month: '2-digit', day: '2-digit' })

const typeLabel = (t: string) => {
  const m: Record<string, string> = {
    SELL_MXN:   'Venta MXN',
    BUY_MXN:    'Compra MXN',
    SELL_GTQ:   'Venta GTQ',
    BUY_GTQ:    'Compra GTQ',
    PAYMENT:    'Abono',
    WITHDRAWAL: 'Retiro',
  }
  return m[t] || t
}
</script>
