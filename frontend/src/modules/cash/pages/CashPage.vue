<template>
  <div class="px-5 py-6 space-y-6">
    <!-- Header Oculto si replicamos el diseño del banner -->
    
    <!-- Loading -->
    <div v-if="loadingCash" class="py-10 text-center text-muted">Cargando...</div>

    <!-- No hay caja abierta -->
    <div v-else-if="noSession || (!currentSession)" class="space-y-6">
      <div class="bg-card border border-border rounded-xl shadow-sm p-8 text-center space-y-4">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-warning-light">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-warning-dark"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/></svg>
        </div>
        <h3 class="text-lg font-bold text-foreground">No hay caja abierta</h3>
        <p class="text-sm text-muted max-w-md mx-auto">
          Para poder registrar transacciones, primero debes abrir una sesión de caja indicando el saldo inicial.
        </p>
        <Button @click="showOpenModal = true">Abrir Caja</Button>
      </div>
    </div>

    <!-- Caja abierta (Rediseño) -->
    <div v-else-if="currentSession && currentSession.status === 'open'" class="space-y-8">
      
      <!-- Top Banner -->
      <div class="bg-card border border-border rounded-xl shadow-sm p-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 relative overflow-hidden">
        <div class="absolute left-0 top-0 bottom-0 w-1 bg-primary"></div>
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-full bg-primary-light/50 flex items-center justify-center text-primary">
            <!-- Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>
          </div>
          <div>
            <div class="flex items-center gap-2 mb-1">
              <h2 class="text-xl font-bold">Caja Principal <span class="text-muted text-lg font-normal">#{{ currentSession.id.split('-')[0].toUpperCase() }}</span></h2>
              <span class="px-2 py-0.5 text-[10px] uppercase font-bold text-success-dark bg-success-light rounded-full">Aperturado</span>
            </div>
            <p class="text-xs text-muted mb-0.5">Responsable: <span class="font-medium text-foreground">{{ userName }}</span></p>
            <p class="text-xs text-muted">Apertura: {{ formatDateTime(currentSession.opened_at) }}</p>
          </div>
        </div>
        <div class="flex-shrink-0">
          <Button @click="showCloseModal = true" class="bg-orange-600 hover:bg-orange-700 text-white border-0 shadow-md flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            Corte Rápido
          </Button>
        </div>
      </div>

      <!-- Acciones Rápidas -->
      <div>
        <h3 class="text-sm font-bold text-foreground mb-4">Acciones Rápidas</h3>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div @click="$router.push('/transactions')" class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow cursor-pointer flex flex-col items-center justify-center text-center group">
            <div class="w-12 h-12 rounded-full bg-primary-light/50 flex items-center justify-center text-primary group-hover:scale-110 transition-transform mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>
            </div>
            <h4 class="font-bold text-sm">Nueva Transacción</h4>
            <p class="text-xs text-muted">Registrar una transacción</p>
          </div>
          <div class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow cursor-pointer flex flex-col items-center justify-center text-center group">
            <div class="w-12 h-12 rounded-full bg-primary-light/50 flex items-center justify-center text-primary group-hover:scale-110 transition-transform mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
            </div>
            <h4 class="font-bold text-sm">Retiro/Fondo</h4>
            <p class="text-xs text-muted">Agregar o retirar efectivo</p>
          </div>
          <div @click="$router.push('/transactions')" class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow cursor-pointer flex flex-col items-center justify-center text-center group">
            <div class="w-12 h-12 rounded-full bg-primary-light/50 flex items-center justify-center text-primary group-hover:scale-110 transition-transform mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            </div>
            <h4 class="font-bold text-sm">Historial</h4>
            <p class="text-xs text-muted">Ver historial de caja</p>
          </div>
        </div>
      </div>

      <!-- Actividad Reciente -->
      <div class="bg-card border border-border rounded-xl shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-border flex justify-between items-center">
          <h3 class="text-sm font-bold">Actividad Reciente</h3>
          <router-link to="/transactions" class="text-xs text-primary hover:underline">Ver historial completo &rarr;</router-link>
        </div>
        <div class="divide-y divide-border">
          <div v-for="txn in recentTransactions" :key="txn.id" class="px-6 py-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-900/50">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-success-light flex items-center justify-center text-success-dark">
                <svg v-if="txn.status === 'ACTIVE'" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" x2="9" y1="9" y2="15"/><line x1="9" x2="15" y1="9" y2="15"/></svg>
              </div>
              <div>
                <p class="text-sm font-medium">{{ typeLabel(txn.transaction_type) }} <span class="font-mono text-xs text-muted">#{{ txn.code.split('-')[1] || txn.code }}</span></p>
                <p class="text-xs text-muted">Cliente UUID: {{ txn.client_id.slice(0, 8) }} • {{ timeAgo(txn.created_at) }}</p>
              </div>
            </div>
            <div class="text-right">
              <!-- MXN -->
              <p v-if="Number(txn.amount_mxn) > 0" class="text-sm font-bold" :class="txn.status === 'ACTIVE' ? 'text-success-dark' : 'text-muted line-through'">
                +${{ formatCurrency(txn.amount_mxn) }}
              </p>
              <!-- GTQ -->
              <p v-if="Number(txn.amount_gtq) > 0" class="text-sm font-bold" :class="txn.status === 'ACTIVE' ? 'text-info-dark' : 'text-muted line-through'">
                +Q{{ formatCurrency(txn.amount_gtq) }}
              </p>
            </div>
          </div>
          <div v-if="recentTransactions.length === 0" class="px-6 py-8 text-center text-sm text-muted">
            No se han registrado transacciones todavía.
          </div>
        </div>
      </div>

      <!-- Resumen de Caja -->
      <div>
        <h3 class="text-sm font-bold text-foreground mb-4">Resumen de Caja</h3>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
          <!-- Saldo Inicial -->
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm">
            <p class="text-xs font-bold text-muted mb-3">Saldo Apertura</p>
            <p class="text-xl font-bold font-mono text-foreground mb-1">
              $ {{ formatCurrency(currentSession.opening_amount_mxn) }}
            </p>
            <p class="text-xl font-bold font-mono text-foreground">
              Q {{ formatCurrency(currentSession.opening_amount_gtq) }}
            </p>
          </div>
          <!-- Operaciones del turno -->
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm">
            <p class="text-xs font-bold text-muted mb-3">Movimiento Neto</p>
            <p class="text-xl font-bold font-mono mb-1"
              :class="cashMovement.mxn >= 0 ? 'text-emerald-600' : 'text-red-600'">
              {{ cashMovement.mxn >= 0 ? '+' : '' }}$ {{ formatCurrency(cashMovement.mxn) }}
            </p>
            <p class="text-xl font-bold font-mono"
              :class="cashMovement.gtq >= 0 ? 'text-emerald-600' : 'text-red-600'">
              {{ cashMovement.gtq >= 0 ? '+' : '' }}Q {{ formatCurrency(cashMovement.gtq) }}
            </p>
          </div>
          <!-- Saldo Esperado (backend) -->
          <div class="bg-card border-2 border-primary rounded-xl p-5 shadow-md bg-primary-light/5">
            <p class="text-xs font-bold text-primary mb-3">Saldo Esperado en Caja</p>
            <p class="text-xl font-bold font-mono text-primary-dark mb-1">
              $ {{ formatCurrency(currentSession.current_amount_mxn) }}
            </p>
            <p class="text-xl font-bold font-mono text-primary-dark">
              Q {{ formatCurrency(currentSession.current_amount_gtq) }}
            </p>
            <p class="text-[10px] text-muted mt-2">Calculado por el sistema</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Cierre Summary / Estado Desconocido como antes -->
    <div v-else-if="currentSession && currentSession.status === 'closed'" class="space-y-6">
       <!-- Reusando logica vieja omitida por brevedad de la request, se retiene el bloque viejo para cajas cerradas -->
      <div class="bg-card border border-border rounded-xl shadow-sm p-8 text-center space-y-4">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-light">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary-dark"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
        </div>
        <h3 class="text-lg font-bold text-foreground">Última caja cerrada</h3>
        <p class="text-sm text-muted">Cerrada el {{ formatDate(currentSession.closed_at!) }}</p>
        <Button @click="showOpenModal = true" class="mt-4">Abrir Nueva Caja</Button>
      </div>
    </div>

    <!-- Modal Abrir (se retiene igual) -->
    <div v-if="showOpenModal" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-card w-full max-w-md rounded-xl shadow-xl border border-border overflow-hidden">
        <div class="px-6 py-4 border-b border-border flex justify-between items-center">
          <h3 class="text-lg font-bold">Abrir Caja</h3>
          <button @click="showOpenModal = false" class="text-muted hover:text-foreground text-xl">&times;</button>
        </div>
        <form @submit.prevent="handleOpen" class="p-6 space-y-4">
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Saldo Inicial MXN</label>
            <input v-model.number="openForm.opening_amount_mxn" type="number" step="0.01" min="0" required class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Saldo Inicial GTQ</label>
            <input v-model.number="openForm.opening_amount_gtq" type="number" step="0.01" min="0" required class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <Button type="button" variant="outline" @click="showOpenModal = false">Cancelar</Button>
            <Button type="submit" :disabled="formLoading">{{ formLoading ? 'Abriendo...' : 'Abrir Caja' }}</Button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Cerrar -->
    <div v-if="showCloseModal" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-card w-full max-w-md rounded-xl shadow-xl border border-border overflow-hidden">
        <div class="px-6 py-4 border-b border-border flex justify-between items-center">
          <h3 class="text-lg font-bold">Corte de Caja (Cierre)</h3>
          <button @click="showCloseModal = false" class="text-muted hover:text-foreground text-xl">&times;</button>
        </div>
        <form @submit.prevent="handleClose" class="p-6 space-y-4">
          <!-- Saldo esperado como referencia -->
          <div class="bg-slate-50 dark:bg-slate-900 border border-border rounded-lg p-4">
            <p class="text-xs font-medium text-muted uppercase mb-2">Saldo esperado por el sistema</p>
            <div class="flex gap-6">
              <div>
                <span class="text-[10px] text-muted">MXN</span>
                <p class="text-lg font-bold font-mono text-foreground">$ {{ formatCurrency(currentSession?.current_amount_mxn) }}</p>
              </div>
              <div>
                <span class="text-[10px] text-muted">GTQ</span>
                <p class="text-lg font-bold font-mono text-foreground">Q {{ formatCurrency(currentSession?.current_amount_gtq) }}</p>
              </div>
            </div>
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Efectivo Físico MXN <span class="text-error">*</span></label>
            <input v-model.number="closeForm.closing_amount_mxn" type="number" step="0.01" min="0" required class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" placeholder="Billetes + monedas MXN" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Efectivo Físico GTQ <span class="text-error">*</span></label>
            <input v-model.number="closeForm.closing_amount_gtq" type="number" step="0.01" min="0" required class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" placeholder="Billetes + monedas GTQ" />
          </div>
          <!-- Preview de diferencia en tiempo real -->
          <div v-if="closeForm.closing_amount_mxn > 0 || closeForm.closing_amount_gtq > 0" class="border rounded-lg p-3" :class="hasDifference ? 'border-amber-300 bg-amber-50 dark:bg-amber-950/30' : 'border-emerald-300 bg-emerald-50 dark:bg-emerald-950/30'">
            <p class="text-xs font-medium mb-1" :class="hasDifference ? 'text-amber-700 dark:text-amber-400' : 'text-emerald-700 dark:text-emerald-400'">
              {{ hasDifference ? '⚠️ Diferencia detectada' : '✓ Cuadre exacto' }}
            </p>
            <div class="flex gap-4 text-sm font-mono font-medium">
              <span :class="closeDiffMxn === 0 ? 'text-muted' : closeDiffMxn > 0 ? 'text-emerald-600' : 'text-red-600'">
                MXN: {{ closeDiffMxn >= 0 ? '+' : '' }}{{ formatCurrency(closeDiffMxn) }}
              </span>
              <span :class="closeDiffGtq === 0 ? 'text-muted' : closeDiffGtq > 0 ? 'text-emerald-600' : 'text-red-600'">
                GTQ: {{ closeDiffGtq >= 0 ? '+' : '' }}{{ formatCurrency(closeDiffGtq) }}
              </span>
            </div>
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Notas Adicionales</label>
            <textarea v-model="closeForm.notes" rows="2" class="w-full px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" placeholder="Justificación de sobrantes/faltantes si hay"></textarea>
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <Button type="button" variant="outline" @click="showCloseModal = false">Cancelar</Button>
            <Button type="submit" class="bg-orange-600 hover:bg-orange-700 text-white" :disabled="formLoading">{{ formLoading ? 'Terminando turno...' : 'Confirmar Corte' }}</Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useCash } from '@/modules/cash/composables/useCash'
import { useTransactions } from '@/modules/transactions/composables/useTransactions'
import { useAuthStore } from '@/modules/auth/stores/authStore'
import { Button } from '@/theme/components/ui/button'

const { currentSession, loading: loadingCash, noSession, fetchCurrent, openCash, closeCash } = useCash()
const { transactions, loadTransactions } = useTransactions()
const authStore = useAuthStore()

const userName = computed(() => authStore.user?.full_name || 'Operador')

const showOpenModal = ref(false)
const showCloseModal = ref(false)
const formLoading = ref(false)

const openForm = reactive({ opening_amount_mxn: 0, opening_amount_gtq: 0, notes: '' })
const closeForm = reactive({ closing_amount_mxn: 0, closing_amount_gtq: 0, notes: '' })

onMounted(async () => {
  await fetchCurrent()
  if (currentSession.value && currentSession.value.status === 'open') {
    await loadTransactions()
  }
})

// Filtrar transacciones del turno actual
const sessionTxns = computed(() => {
  if (!currentSession.value) return []
  return transactions.value.filter(t => t.cash_session_id === currentSession.value!.id)
})

const recentTransactions = computed(() => {
  return sessionTxns.value.slice(0, 5)
})

// Movimiento neto = current - opening (lo que cambió durante el turno)
const cashMovement = computed(() => {
  if (!currentSession.value) return { mxn: 0, gtq: 0 }
  return {
    mxn: Number(currentSession.value.current_amount_mxn || 0) - Number(currentSession.value.opening_amount_mxn || 0),
    gtq: Number(currentSession.value.current_amount_gtq || 0) - Number(currentSession.value.opening_amount_gtq || 0),
  }
})

// Preview de diferencia en el modal de cierre
const closeDiffMxn = computed(() => {
  return (closeForm.closing_amount_mxn || 0) - Number(currentSession.value?.current_amount_mxn || 0)
})
const closeDiffGtq = computed(() => {
  return (closeForm.closing_amount_gtq || 0) - Number(currentSession.value?.current_amount_gtq || 0)
})
const hasDifference = computed(() => {
  return Math.abs(closeDiffMxn.value) > 0.01 || Math.abs(closeDiffGtq.value) > 0.01
})

const formatCurrency = (val?: string | number | null) => {
  if (val === undefined || val === null) return '0.00'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateString: string) => new Date(dateString).toLocaleDateString('es-ES')
const formatDateTime = (dateString: string) => {
  const d = new Date(dateString)
  return d.toLocaleDateString('es-ES', { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' }) + ', ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

const timeAgo = (dateString: string) => {
  const r = new Date(dateString)
  return r.toLocaleTimeString() // simpler fallback
}

const typeLabel = (t: string) => {
  const ms: Record<string,string> = { SELL_MXN: 'Venta MXN', BUY_MXN: 'Compra MXN', SELL_GTQ: 'Venta GTQ', BUY_GTQ: 'Compra GTQ' }
  return ms[t] || t
}

async function handleOpen() {
  formLoading.value = true
  try {
    await openCash(openForm)
    showOpenModal.value = false
    await loadTransactions()
  } finally { formLoading.value = false }
}

async function handleClose() {
  if (!currentSession.value) return
  formLoading.value = true
  try {
    await closeCash(currentSession.value.id, closeForm)
    showCloseModal.value = false
  } finally { formLoading.value = false }
}
</script>
