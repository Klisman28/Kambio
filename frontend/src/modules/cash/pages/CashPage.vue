<template>
  <div class="px-5 py-6 space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-foreground">Caja</h1>
      <p class="text-sm text-muted">Control de apertura y cierre de sesión de caja</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="py-10 text-center text-muted">Cargando...</div>

    <!-- No hay caja abierta -->
    <div v-else-if="noSession || (!currentSession)" class="space-y-6">
      <div class="bg-card border border-border rounded-xl shadow-sm p-8 text-center space-y-4">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-warning-light">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-warning-dark"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/></svg>
        </div>
        <h3 class="text-lg font-bold text-foreground">No hay caja abierta</h3>
        <p class="text-sm text-muted max-w-md mx-auto">
          Para poder registrar transacciones, primero debes abrir una sesión de caja indicando el saldo inicial en ambas divisas.
        </p>
        <Button @click="showOpenModal = true">Abrir Caja</Button>
      </div>
    </div>

    <!-- Caja abierta -->
    <div v-else-if="currentSession && currentSession.status === 'open'" class="space-y-6">
      <!-- Status Banner -->
      <div class="bg-success-light border border-success/30 rounded-xl p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div class="flex items-center gap-3">
          <div class="w-3 h-3 rounded-full bg-success animate-pulse"></div>
          <div>
            <p class="font-bold text-success-dark">Caja Abierta</p>
            <p class="text-xs text-success-dark/70">Desde {{ formatDate(currentSession.opened_at) }}</p>
          </div>
        </div>
        <Button variant="outline" @click="showCloseModal = true" class="border-error text-error hover:bg-error-light">
          Cerrar Caja
        </Button>
      </div>

      <!-- Saldos de Apertura -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div class="bg-card border border-border rounded-xl p-6 shadow-sm">
          <p class="text-sm font-medium text-muted mb-1">Saldo Apertura MXN</p>
          <h3 class="text-2xl font-bold text-foreground font-mono">$ {{ formatCurrency(currentSession.opening_amount_mxn) }}</h3>
        </div>
        <div class="bg-card border border-border rounded-xl p-6 shadow-sm">
          <p class="text-sm font-medium text-muted mb-1">Saldo Apertura GTQ</p>
          <h3 class="text-2xl font-bold text-foreground font-mono">Q {{ formatCurrency(currentSession.opening_amount_gtq) }}</h3>
        </div>
      </div>

      <!-- Notas -->
      <div v-if="currentSession.notes" class="bg-card border border-border rounded-xl p-5 shadow-sm">
        <p class="text-sm font-medium text-muted mb-1">Notas</p>
        <p class="text-sm text-foreground">{{ currentSession.notes }}</p>
      </div>
    </div>

    <!-- Caja cerrada (último cierre) -->
    <div v-else-if="currentSession && currentSession.status === 'closed'" class="space-y-6">
      <div class="bg-card border border-border rounded-xl shadow-sm p-8 text-center space-y-4">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-light">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary-dark"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
        </div>
        <h3 class="text-lg font-bold text-foreground">Última caja cerrada</h3>
        <p class="text-sm text-muted">
          Cerrada el {{ formatDate(currentSession.closed_at!) }}
        </p>

        <!-- Resumen de cierre -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4 text-left max-w-2xl mx-auto">
          <div class="bg-background border border-border rounded-lg p-3">
            <p class="text-[10px] text-muted uppercase font-semibold">Apertura MXN</p>
            <p class="font-mono font-bold text-sm">$ {{ formatCurrency(currentSession.opening_amount_mxn) }}</p>
          </div>
          <div class="bg-background border border-border rounded-lg p-3">
            <p class="text-[10px] text-muted uppercase font-semibold">Apertura GTQ</p>
            <p class="font-mono font-bold text-sm">Q {{ formatCurrency(currentSession.opening_amount_gtq) }}</p>
          </div>
          <div class="bg-background border border-border rounded-lg p-3">
            <p class="text-[10px] text-muted uppercase font-semibold">Cierre MXN</p>
            <p class="font-mono font-bold text-sm">$ {{ formatCurrency(currentSession.closing_amount_mxn) }}</p>
          </div>
          <div class="bg-background border border-border rounded-lg p-3">
            <p class="text-[10px] text-muted uppercase font-semibold">Cierre GTQ</p>
            <p class="font-mono font-bold text-sm">Q {{ formatCurrency(currentSession.closing_amount_gtq) }}</p>
          </div>
        </div>

        <!-- Diferencias -->
        <div class="grid grid-cols-2 gap-4 max-w-md mx-auto mt-2">
          <div class="p-3 rounded-lg" :class="diffClass(currentSession.difference_mxn)">
            <p class="text-[10px] uppercase font-semibold">Diferencia MXN</p>
            <p class="font-mono font-bold text-sm">$ {{ formatCurrency(currentSession.difference_mxn) }}</p>
          </div>
          <div class="p-3 rounded-lg" :class="diffClass(currentSession.difference_gtq)">
            <p class="text-[10px] uppercase font-semibold">Diferencia GTQ</p>
            <p class="font-mono font-bold text-sm">Q {{ formatCurrency(currentSession.difference_gtq) }}</p>
          </div>
        </div>

        <Button @click="showOpenModal = true" class="mt-4">Abrir Nueva Caja</Button>
      </div>
    </div>
    
    <!-- Fallback default just in case -->
    <div v-else class="space-y-6">
      <div class="bg-error-light border border-error/30 rounded-xl p-8 text-center space-y-4">
        <h3 class="text-lg font-bold text-error-dark">Estado de caja desconocido</h3>
        <p class="text-sm text-error-dark/70">
          La caja retornó un estado inesperado: {{ currentSession?.status }}
        </p>
        <Button @click="showOpenModal = true" variant="outline" class="border-error text-error hover:bg-error-light">Forzar Apertura</Button>
      </div>
    </div>

    <!-- Modal: Abrir Caja -->
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
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Notas (opcional)</label>
            <textarea v-model="openForm.notes" rows="2" class="w-full px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary"></textarea>
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <Button type="button" variant="outline" @click="showOpenModal = false">Cancelar</Button>
            <Button type="submit" :disabled="formLoading">{{ formLoading ? 'Abriendo...' : 'Abrir Caja' }}</Button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal: Cerrar Caja -->
    <div v-if="showCloseModal" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-card w-full max-w-md rounded-xl shadow-xl border border-border overflow-hidden">
        <div class="px-6 py-4 border-b border-border flex justify-between items-center">
          <h3 class="text-lg font-bold">Cerrar Caja</h3>
          <button @click="showCloseModal = false" class="text-muted hover:text-foreground text-xl">&times;</button>
        </div>
        <form @submit.prevent="handleClose" class="p-6 space-y-4">
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Saldo Final MXN</label>
            <input v-model.number="closeForm.closing_amount_mxn" type="number" step="0.01" min="0" required class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Saldo Final GTQ</label>
            <input v-model.number="closeForm.closing_amount_gtq" type="number" step="0.01" min="0" required class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Notas (opcional)</label>
            <textarea v-model="closeForm.notes" rows="2" class="w-full px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary"></textarea>
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <Button type="button" variant="outline" @click="showCloseModal = false">Cancelar</Button>
            <Button type="submit" :disabled="formLoading">{{ formLoading ? 'Cerrando...' : 'Cerrar Caja' }}</Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useCash } from '@/modules/cash/composables/useCash'
import { Button } from '@/theme/components/ui/button'

const { currentSession, loading, noSession, fetchCurrent, openCash, closeCash } = useCash()

const showOpenModal = ref(false)
const showCloseModal = ref(false)
const formLoading = ref(false)

const openForm = reactive({
  opening_amount_mxn: 0,
  opening_amount_gtq: 0,
  notes: '',
})

const closeForm = reactive({
  closing_amount_mxn: 0,
  closing_amount_gtq: 0,
  notes: '',
})

onMounted(() => fetchCurrent())

const formatCurrency = (val?: string | number | null) => {
  if (val === undefined || val === null) return '0.00'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

const diffClass = (val?: string | number | null) => {
  const n = Number(val || 0)
  if (n > 0) return 'bg-success-light text-success-dark'
  if (n < 0) return 'bg-error-light text-error-dark'
  return 'bg-primary-light text-primary-dark'
}

async function handleOpen() {
  formLoading.value = true
  try {
    await openCash({
      opening_amount_mxn: openForm.opening_amount_mxn,
      opening_amount_gtq: openForm.opening_amount_gtq,
      notes: openForm.notes || undefined,
    })
    showOpenModal.value = false
  } catch { /* handled by composable */ } finally {
    formLoading.value = false
  }
}

async function handleClose() {
  if (!currentSession.value) return
  formLoading.value = true
  try {
    await closeCash(currentSession.value.id, {
      closing_amount_mxn: closeForm.closing_amount_mxn,
      closing_amount_gtq: closeForm.closing_amount_gtq,
      notes: closeForm.notes || undefined,
    })
    showCloseModal.value = false
  } catch { /* handled by composable */ } finally {
    formLoading.value = false
  }
}
</script>
