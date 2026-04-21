<template>
  <div class="px-5 py-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <Button variant="outline" size="sm" @click="$router.push('/clients')" class="mb-2">
          ← Volver
        </Button>
        <h1 class="text-2xl font-bold">Detalle del Cliente</h1>
      </div>
    </div>

    <div v-if="loading" class="text-center py-10 text-muted text-sm">Cargando...</div>

    <div v-else-if="client" class="grid grid-cols-1 md:grid-cols-3 gap-6">

      <!-- ─── Columna izquierda: perfil + posición ─── -->
      <div class="bg-background border border-border rounded-xl p-6 shadow-sm col-span-1 space-y-5">

        <!-- Datos básicos -->
        <div>
          <div class="w-10 h-10 rounded-xl bg-primary-light flex items-center justify-center text-primary mb-3 text-base font-bold">
            {{ initials(client.full_name) }}
          </div>
          <h3 class="font-bold text-lg leading-tight">{{ client.full_name }}</h3>
          <p class="text-xs text-muted font-mono mb-3">{{ client.code }}</p>
          <div class="space-y-1 text-sm">
            <p class="text-muted">Email: <span class="text-foreground">{{ client.email || '—' }}</span></p>
            <p class="text-muted">Estado:
              <span :class="client.is_active ? 'text-emerald-600 font-semibold' : 'text-red-500 font-semibold'">
                {{ client.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </p>
          </div>
        </div>

        <hr class="border-border" />

        <!-- Posición financiera — grid 2 columnas side by side -->
        <div>
          <h4 class="text-xs font-semibold text-muted uppercase tracking-wide mb-3">Posición Financiera</h4>

          <div v-if="normalizedBalance" class="grid grid-cols-2 gap-2">

            <!-- MXN -->
            <div class="border rounded-xl p-3 space-y-1"
              :class="normalizedBalance.mxn.position === 'COMPANY_OWES' ? 'border-red-200 dark:border-red-900 bg-red-50/30 dark:bg-red-950/10'
                     : normalizedBalance.mxn.position === 'CLIENT_OWES' ? 'border-emerald-200 dark:border-emerald-900 bg-emerald-50/20 dark:bg-emerald-950/10'
                     : 'border-border'">
              <p class="text-[10px] font-mono font-semibold text-muted">MXN</p>
              <p class="text-lg font-bold font-mono leading-tight"
                :class="positionColorClass(normalizedBalance.mxn.position)">
                ${{ fmtAmount(normalizedBalance.mxn.absolute_balance) }}
              </p>
              <p class="text-[10px] font-medium" :class="positionColorClass(normalizedBalance.mxn.position)">
                {{ normalizedBalance.mxn.display_label }}
              </p>
            </div>

            <!-- GTQ -->
            <div class="border rounded-xl p-3 space-y-1"
              :class="normalizedBalance.gtq.position === 'COMPANY_OWES' ? 'border-red-200 dark:border-red-900 bg-red-50/30 dark:bg-red-950/10'
                     : normalizedBalance.gtq.position === 'CLIENT_OWES' ? 'border-emerald-200 dark:border-emerald-900 bg-emerald-50/20 dark:bg-emerald-950/10'
                     : 'border-border'">
              <p class="text-[10px] font-mono font-semibold text-muted">GTQ</p>
              <p class="text-lg font-bold font-mono leading-tight"
                :class="positionColorClass(normalizedBalance.gtq.position)">
                Q{{ fmtAmount(normalizedBalance.gtq.absolute_balance) }}
              </p>
              <p class="text-[10px] font-medium" :class="positionColorClass(normalizedBalance.gtq.position)">
                {{ normalizedBalance.gtq.display_label }}
              </p>
            </div>

          </div>
          <div v-else class="text-sm text-muted">No disponible</div>
        </div>

        <!-- Resumen rápido de ledger (del summary) -->
        <div v-if="ledgerSummary" class="space-y-2">
          <h4 class="text-xs font-semibold text-muted uppercase tracking-wide">Movimientos del período</h4>
          <div class="grid grid-cols-2 gap-2 text-[11px]">
            <div class="flex flex-col gap-0.5">
              <span class="text-muted">Egreso MXN</span>
              <span class="font-mono font-semibold text-red-600 dark:text-red-400">
                −${{ fmtAmount(ledgerSummary.total_egreso_mxn) }}
              </span>
            </div>
            <div class="flex flex-col gap-0.5">
              <span class="text-muted">Ingreso MXN</span>
              <span class="font-mono font-semibold text-emerald-600 dark:text-emerald-400">
                +${{ fmtAmount(ledgerSummary.total_ingreso_mxn) }}
              </span>
            </div>
            <div class="flex flex-col gap-0.5">
              <span class="text-muted">Egreso GTQ</span>
              <span class="font-mono font-semibold text-red-600 dark:text-red-400">
                −Q{{ fmtAmount(ledgerSummary.total_egreso_gtq) }}
              </span>
            </div>
            <div class="flex flex-col gap-0.5">
              <span class="text-muted">Ingreso GTQ</span>
              <span class="font-mono font-semibold text-emerald-600 dark:text-emerald-400">
                +Q{{ fmtAmount(ledgerSummary.total_ingreso_gtq) }}
              </span>
            </div>
          </div>
        </div>

      </div>

      <!-- ─── Columna derecha: Libro Mayor agrupado ─── -->
      <div class="bg-background border border-border rounded-xl p-6 shadow-sm col-span-1 md:col-span-2">
        <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="font-bold text-lg">Libro Mayor</h3>
            <p class="text-xs text-muted">Últimas transacciones</p>
          </div>
          <Button variant="default" size="sm" @click="$router.push(`/ledger/${clientId}?from=clients`)" class="gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
            Ver completo
          </Button>
        </div>

        <!-- Tabla con el formato agrupado: 1 fila por transacción -->
        <div v-if="groupedRows.length" class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr class="bg-muted/5 border-b border-border">
                <th class="text-left text-[11px] font-semibold uppercase tracking-wide text-muted px-3 py-2.5 whitespace-nowrap">Fecha</th>
                <th class="text-left text-[11px] font-semibold uppercase tracking-wide text-muted px-3 py-2.5">Operación</th>
                <th class="text-right text-[11px] font-semibold uppercase tracking-wide text-red-500/70 px-3 py-2.5 bg-red-50/30 dark:bg-red-950/10">Egreso MXN</th>
                <th class="text-right text-[11px] font-semibold uppercase tracking-wide text-red-500/70 px-3 py-2.5 bg-red-50/30 dark:bg-red-950/10">Egreso GTQ</th>
                <th class="text-right text-[11px] font-semibold uppercase tracking-wide text-emerald-600/70 px-3 py-2.5 bg-emerald-50/30 dark:bg-emerald-950/10">Ingreso MXN</th>
                <th class="text-right text-[11px] font-semibold uppercase tracking-wide text-emerald-600/70 px-3 py-2.5 bg-emerald-50/30 dark:bg-emerald-950/10">Ingreso GTQ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in groupedRows" :key="row.transaction_id"
                class="border-b border-border/50 hover:bg-muted/5 transition-colors">
                <td class="px-3 py-2.5 text-muted whitespace-nowrap tabular-nums">
                  {{ formatDate(row.date) }}
                </td>
                <td class="px-3 py-2.5 font-medium text-foreground">
                  {{ typeLabel(row.operation) }}
                  <span class="block font-mono text-[10px] text-muted/60 font-normal">{{ row.reference }}</span>
                </td>
                <td class="px-3 py-2.5 text-right tabular-nums bg-red-50/20 dark:bg-red-950/5">
                  <span v-if="Number(row.egreso_mxn) > 0" class="font-mono font-medium text-red-600 dark:text-red-400">
                    ${{ fmtAmount(row.egreso_mxn) }}
                  </span>
                  <span v-else class="text-muted/30">—</span>
                </td>
                <td class="px-3 py-2.5 text-right tabular-nums bg-red-50/20 dark:bg-red-950/5">
                  <span v-if="Number(row.egreso_gtq) > 0" class="font-mono font-medium text-red-600 dark:text-red-400">
                    Q{{ fmtAmount(row.egreso_gtq) }}
                  </span>
                  <span v-else class="text-muted/30">—</span>
                </td>
                <td class="px-3 py-2.5 text-right tabular-nums bg-emerald-50/20 dark:bg-emerald-950/5">
                  <span v-if="Number(row.ingreso_mxn) > 0" class="font-mono font-medium text-emerald-600 dark:text-emerald-400">
                    ${{ fmtAmount(row.ingreso_mxn) }}
                  </span>
                  <span v-else class="text-muted/30">—</span>
                </td>
                <td class="px-3 py-2.5 text-right tabular-nums bg-emerald-50/20 dark:bg-emerald-950/5">
                  <span v-if="Number(row.ingreso_gtq) > 0" class="font-mono font-medium text-emerald-600 dark:text-emerald-400">
                    Q{{ fmtAmount(row.ingreso_gtq) }}
                  </span>
                  <span v-else class="text-muted/30">—</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-center py-8 text-sm text-muted">No hay movimientos registrados.</p>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Button } from '@/theme/components/ui/button'
import http from '@/services/http'
import type { Client } from '@/modules/clients/composables/useClients'
import type { BalanceOut, CurrencyBalance, LedgerGroupedRow, LedgerGroupedSummary } from '@/types/ledger'
import { positionColorClass, fmtAmount } from '@/types/ledger'

const route    = useRoute()
const clientId = route.params.id as string

const client   = ref<Client | null>(null)
const balance  = ref<any | null>(null)
const ledgerSummary = ref<LedgerGroupedSummary | null>(null)
const groupedRows   = ref<LedgerGroupedRow[]>([])
const loading  = ref(true)

// Iniciales del nombre para el avatar
const initials = (name: string) => name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase()

// Normaliza balance viejo {mxn: "363"} o nuevo {mxn: CurrencyBalance}
function makeBalance(raw: number): CurrencyBalance {
  if (raw > 0) return { raw_balance: raw, absolute_balance: raw, position: 'CLIENT_OWES', display_label: 'El cliente debe' }
  if (raw < 0) return { raw_balance: raw, absolute_balance: Math.abs(raw), position: 'COMPANY_OWES', display_label: 'A favor del cliente' }
  return { raw_balance: 0, absolute_balance: 0, position: 'SETTLED', display_label: 'Saldado' }
}

const normalizedBalance = computed<BalanceOut | null>(() => {
  if (!balance.value) return null
  const b = balance.value
  if (b.mxn && typeof b.mxn === 'object' && 'position' in b.mxn) return b as BalanceOut
  return {
    client_id: b.client_id,
    mxn: makeBalance(Number(b.mxn) || 0),
    gtq: makeBalance(Number(b.gtq) || 0),
    equivalent_in_mxn: null,
    equivalent_in_gtq: null,
    reference_exchange_rate: null,
  } as BalanceOut
})

const formatDate = (d: string) =>
  new Date(d).toLocaleDateString('es-GT', { year: 'numeric', month: '2-digit', day: '2-digit' })

const typeLabel = (t: string) => {
  const m: Record<string, string> = {
    SELL_MXN: 'Venta MXN', BUY_MXN: 'Compra MXN',
    SELL_GTQ: 'Venta GTQ', BUY_GTQ: 'Compra GTQ',
    PAYMENT: 'Abono', WITHDRAWAL: 'Retiro',
  }
  return m[t] || t
}

onMounted(async () => {
  try {
    const [clientRes, balRes, summaryRes] = await Promise.all([
      http.get(`/api/v1/clients/${clientId}`),
      http.get(`/api/v1/clients/${clientId}/balance`),
      // Nuevo endpoint agrupado: 1 fila por transacción
      http.get(`/api/v1/clients/${clientId}/ledger-summary?limit=8`),
    ])
    client.value       = clientRes.data
    balance.value      = balRes.data
    ledgerSummary.value = summaryRes.data.summary || null
    groupedRows.value  = summaryRes.data.rows || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>
