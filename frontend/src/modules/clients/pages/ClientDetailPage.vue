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

    <div v-if="loading" class="text-center py-10 text-muted text-sm">Cargando...</div>

    <div v-else-if="client" class="grid grid-cols-1 md:grid-cols-3 gap-6">

      <!-- Perfil + Posición financiera -->
      <div class="bg-background border border-border rounded-xl p-6 shadow-sm col-span-1 space-y-5">
        <!-- Datos básicos -->
        <div>
          <h3 class="font-bold text-lg mb-1">{{ client.full_name }}</h3>
          <p class="text-xs text-muted font-mono mb-3">{{ client.code }}</p>
          <div class="space-y-1 text-sm">
            <p class="text-muted">Email: <span class="text-foreground">{{ client.email || '—' }}</span></p>
            <p class="text-muted">Estado:
              <span :class="client.is_active ? 'text-emerald-600' : 'text-red-500'">
                {{ client.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </p>
          </div>
        </div>

        <hr class="border-border" />

        <!-- Posición financiera -->
        <div>
          <h4 class="text-xs font-semibold text-muted uppercase tracking-wide mb-3">Posición Financiera</h4>

          <!-- MXN -->
          <div v-if="normalizedBalance" class="space-y-2">
            <div class="border border-border rounded-lg p-3">
              <div class="flex items-center justify-between mb-1">
                <span class="text-[10px] font-mono font-medium text-muted">MXN</span>
                <span class="text-[10px] font-medium px-1.5 py-0.5 rounded"
                  :class="positionBadgeClass(normalizedBalance.mxn.position)">
                  {{ normalizedBalance.mxn.display_label }}
                </span>
              </div>
              <p class="text-xl font-bold font-mono" :class="positionColorClass(normalizedBalance.mxn.position)">
                $ {{ fmtAmount(normalizedBalance.mxn.absolute_balance) }}
              </p>
              <!-- Equivalencia referencial -->
              <p v-if="normalizedBalance.equivalent_in_gtq" class="text-[10px] text-muted mt-1">
                ≈ Q {{ fmtAmount(normalizedBalance.equivalent_in_gtq) }} <span class="italic">(ref.)</span>
              </p>
            </div>

            <!-- GTQ -->
            <div class="border border-border rounded-lg p-3">
              <div class="flex items-center justify-between mb-1">
                <span class="text-[10px] font-mono font-medium text-muted">GTQ</span>
                <span class="text-[10px] font-medium px-1.5 py-0.5 rounded"
                  :class="positionBadgeClass(normalizedBalance.gtq.position)">
                  {{ normalizedBalance.gtq.display_label }}
                </span>
              </div>
              <p class="text-xl font-bold font-mono" :class="positionColorClass(normalizedBalance.gtq.position)">
                Q {{ fmtAmount(normalizedBalance.gtq.absolute_balance) }}
              </p>
              <!-- Equivalencia referencial -->
              <p v-if="normalizedBalance.equivalent_in_mxn" class="text-[10px] text-muted mt-1">
                ≈ $ {{ fmtAmount(normalizedBalance.equivalent_in_mxn) }} <span class="italic">(ref.)</span>
              </p>
            </div>
          </div>
          <div v-else class="text-sm text-muted">No disponible</div>
        </div>
      </div>

      <!-- Libro Mayor (vista reducida) -->
      <div class="bg-background border border-border rounded-xl p-6 shadow-sm col-span-1 md:col-span-2">
        <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="font-bold text-lg">Libro Mayor</h3>
            <p class="text-xs text-muted">Últimos movimientos</p>
          </div>
          <Button variant="default" size="sm" @click="$router.push(`/ledger/${clientId}?from=clients`)" class="gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
            Abrir Libro Mayor Completo
          </Button>
        </div>

        <Table v-if="ledger.length">
          <TableHeader>
            <TableRow class="bg-muted/5">
              <TableHead class="text-[11px] uppercase text-muted py-2.5">Fecha</TableHead>
              <TableHead class="text-[11px] uppercase text-muted py-2.5">Divisa</TableHead>
              <TableHead class="text-[11px] uppercase text-muted py-2.5">Operación</TableHead>
              <TableHead class="text-[11px] uppercase text-muted text-right py-2.5">Monto</TableHead>
              <TableHead class="text-[11px] uppercase text-muted text-right py-2.5">Saldo</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="entry in ledger" :key="entry.id" class="hover:bg-muted/5 transition-colors">
              <TableCell class="text-xs whitespace-nowrap text-muted py-2.5">{{ formatDate(entry.created_at) }}</TableCell>
              <TableCell class="text-xs font-mono font-medium py-2.5">{{ entry.currency }}</TableCell>
              <TableCell class="py-2.5">
                <div class="flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full flex-shrink-0"
                    :class="entry.direction === 'CREDIT' ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                  <span class="text-xs" :class="entry.direction === 'CREDIT' ? 'text-emerald-600 dark:text-emerald-400' : 'text-foreground'">
                    {{ entry.direction === 'CREDIT' ? 'Abono (+)' : 'Cargo (-)' }}
                  </span>
                </div>
              </TableCell>
              <TableCell class="text-right font-mono text-xs tabular-nums py-2.5">{{ fmtAmount(entry.amount) }}</TableCell>
              <TableCell class="text-right font-mono text-xs tabular-nums py-2.5"
                :class="Number(entry.balance_after) < 0 ? 'text-red-600 dark:text-red-400' : 'text-foreground'">
                {{ fmtAmount(entry.balance_after) }}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <p v-else class="text-center py-8 text-sm text-muted">No hay movimientos registrados.</p>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Button } from '@/theme/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/theme/components/ui/table'
import http from '@/services/http'
import type { Client } from '@/modules/clients/composables/useClients'
import type { BalanceOut, LedgerEntryOut } from '@/types/ledger'
import { positionColorClass, positionBadgeClass, fmtAmount } from '@/types/ledger'

const route = useRoute()
const clientId = route.params.id as string

const client = ref<Client | null>(null)
const balance = ref<any | null>(null)
const ledger = ref<LedgerEntryOut[]>([])
const loading = ref(true)

// Normaliza el balance ya sea formato viejo {mxn: "363", gtq: "-1583"}
// o nuevo {mxn: CurrencyBalance, gtq: CurrencyBalance}
function makeBalanceFromNumber(raw: number): CurrencyBalance {
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
    mxn: makeBalanceFromNumber(Number(b.mxn) || 0),
    gtq: makeBalanceFromNumber(Number(b.gtq) || 0),
    equivalent_in_mxn: null,
    equivalent_in_gtq: null,
    reference_exchange_rate: null,
  } as BalanceOut
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-GT', {
    year: 'numeric', month: '2-digit', day: '2-digit'
  })
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
    console.debug('[ClientDetail] balance raw:', JSON.stringify(balRes.data))
    ledger.value = ledRes.data.entries || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>
