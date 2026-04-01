<template>
  <div class="px-5 py-6 space-y-6">
    <!-- Header -->
    <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-foreground">Transacciones</h1>
        <p class="text-sm text-muted">Historial de operaciones de cambio y movimientos</p>
      </div>
      <Button @click="openCreateModal">+ Nueva Transacción</Button>
    </div>

    <!-- Table -->
    <div class="bg-card border border-border rounded-xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <Table v-if="transactions.length > 0">
          <TableHeader>
            <TableRow>
              <TableHead>Código</TableHead>
              <TableHead>Cliente</TableHead>
              <TableHead>Tipo</TableHead>
              <TableHead class="text-right">MXN</TableHead>
              <TableHead class="text-right">GTQ</TableHead>
              <TableHead class="text-right">Comisión</TableHead>
              <TableHead class="text-right">T/C</TableHead>
              <TableHead>Estado</TableHead>
              <TableHead>Fecha</TableHead>
              <TableHead class="text-right">Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="txn in transactions" :key="txn.id">
              <TableCell class="font-mono text-xs text-primary whitespace-nowrap">{{ txn.code }}</TableCell>
              <TableCell class="font-medium whitespace-nowrap">{{ clientName(txn.client_id) }}</TableCell>
              <TableCell>
                <span class="px-2 py-0.5 text-[10px] uppercase font-bold rounded-full" :class="typeClass(txn.transaction_type)">
                  {{ typeLabel(txn.transaction_type) }}
                </span>
              </TableCell>
              <TableCell class="text-right font-mono">{{ fmt(txn.amount_mxn) }}</TableCell>
              <TableCell class="text-right font-mono">{{ fmt(txn.amount_gtq) }}</TableCell>
              <TableCell class="text-right font-mono">{{ fmt(txn.commission) }}</TableCell>
              <TableCell class="text-right font-mono text-xs">{{ txn.exchange_rate ? Number(txn.exchange_rate).toFixed(4) : '—' }}</TableCell>
              <TableCell>
                <span v-if="txn.status === 'ACTIVE'" class="px-2 py-0.5 text-[10px] uppercase font-bold text-success-dark bg-success-light rounded-full">Activa</span>
                <span v-else class="px-2 py-0.5 text-[10px] uppercase font-bold text-error-dark bg-error-light rounded-full">Anulada</span>
              </TableCell>
              <TableCell class="text-xs whitespace-nowrap text-muted">{{ formatDate(txn.created_at) }}</TableCell>
              <TableCell class="text-right">
                <Button
                  v-if="txn.status === 'ACTIVE'"
                  size="sm"
                  variant="outline"
                  class="text-error border-error hover:bg-error-light text-xs"
                  @click="startVoid(txn)"
                >
                  Anular
                </Button>
                <span v-else class="text-xs text-muted">{{ txn.void_reason }}</span>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

      <div v-if="loading" class="p-6 text-center text-muted">Cargando transacciones...</div>
      <div v-if="!loading && transactions.length === 0" class="p-6 text-center text-muted">
        No hay transacciones registradas. Asegúrate de tener una caja abierta.
      </div>
    </div>

    <!-- Modal: Nueva Transacción -->
    <div v-if="showCreateModal" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-card w-full max-w-lg rounded-xl shadow-xl border border-border overflow-hidden flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-border flex justify-between items-center">
          <h3 class="text-lg font-bold">Nueva Transacción</h3>
          <button @click="showCreateModal = false" class="text-muted hover:text-foreground text-xl">&times;</button>
        </div>
        <form @submit.prevent="handleCreate" class="p-6 space-y-4 overflow-y-auto">
          <!-- Cliente -->
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Cliente *</label>
            <select v-model="createForm.client_id" required class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary">
              <option value="" disabled>Seleccionar cliente</option>
              <option v-for="c in clientsList" :key="c.id" :value="c.id">{{ c.full_name }} ({{ c.code }})</option>
            </select>
          </div>

          <!-- Tipo -->
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Tipo de Operación *</label>
            <select v-model="createForm.transaction_type" required class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary">
              <option value="" disabled>Seleccionar tipo</option>
              <option value="SELL_MXN">Venta MXN (cliente recibe MXN, entrega GTQ)</option>
              <option value="BUY_MXN">Compra MXN (cliente entrega MXN, recibe GTQ)</option>
              <option value="PAYMENT">Abono (una divisa)</option>
              <option value="WITHDRAWAL">Retiro (una divisa)</option>
            </select>
          </div>

          <!-- Montos -->
          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-muted">Monto MXN</label>
              <input v-model.number="createForm.amount_mxn" type="number" step="0.01" min="0" class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
            </div>
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-muted">Monto GTQ</label>
              <input v-model.number="createForm.amount_gtq" type="number" step="0.01" min="0" class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
            </div>
          </div>

          <!-- Comisión y Tipo de Cambio -->
          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-muted">Comisión</label>
              <input v-model.number="createForm.commission" type="number" step="0.01" min="0" class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
            </div>
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-muted">Tipo de Cambio</label>
              <input v-model.number="createForm.exchange_rate" type="number" step="0.0001" min="0" placeholder="Opcional" class="w-full h-10 px-3 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
            </div>
          </div>

          <!-- Notas -->
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Notas</label>
            <textarea v-model="createForm.notes" rows="2" class="w-full px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary"></textarea>
          </div>

          <div class="flex justify-end gap-3 pt-2">
            <Button type="button" variant="outline" @click="showCreateModal = false">Cancelar</Button>
            <Button type="submit" :disabled="formLoading">{{ formLoading ? 'Registrando...' : 'Registrar' }}</Button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal: Anular -->
    <div v-if="showVoidModal" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-card w-full max-w-sm rounded-xl shadow-xl border border-border overflow-hidden">
        <div class="px-6 py-4 border-b border-border">
          <h3 class="text-lg font-bold">Anular Transacción</h3>
          <p class="text-xs text-muted mt-1">{{ voidTarget?.code }}</p>
        </div>
        <form @submit.prevent="handleVoid" class="p-6 space-y-4">
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-muted">Motivo de anulación *</label>
            <textarea v-model="voidReason" rows="3" required class="w-full px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary"></textarea>
          </div>
          <div class="flex justify-end gap-3">
            <Button type="button" variant="outline" @click="showVoidModal = false">Cancelar</Button>
            <Button type="submit" :disabled="formLoading" class="bg-error hover:bg-error-dark text-white">
              {{ formLoading ? 'Anulando...' : 'Confirmar Anulación' }}
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useTransactions, type Transaction } from '@/modules/transactions/composables/useTransactions'
import { useClients } from '@/modules/clients/composables/useClients'
import { Button } from '@/theme/components/ui/button'
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/theme/components/ui/table'

const { transactions, loading, loadTransactions, createTransaction, voidTransaction } = useTransactions()
const { clients: clientsList, loadClients } = useClients()

const showCreateModal = ref(false)
const showVoidModal = ref(false)
const formLoading = ref(false)
const voidTarget = ref<Transaction | null>(null)
const voidReason = ref('')

const createForm = reactive({
  client_id: '',
  transaction_type: '',
  amount_mxn: 0,
  amount_gtq: 0,
  commission: 0,
  exchange_rate: undefined as number | undefined,
  notes: '',
})

onMounted(async () => {
  await Promise.all([loadTransactions(), loadClients()])
})

// Map client_id → name
const clientMap = computed(() => {
  const map: Record<string, string> = {}
  clientsList.value.forEach(c => { map[c.id] = c.full_name })
  return map
})
const clientName = (id: string) => clientMap.value[id] || id.slice(0, 8)

const fmt = (val?: string | number | null) => {
  if (!val || Number(val) === 0) return '—'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (d: string) => new Date(d).toLocaleString()

const typeLabel = (t: string) => {
  const m: Record<string, string> = {
    SELL_MXN: 'Venta MXN',
    BUY_MXN: 'Compra MXN',
    PAYMENT: 'Abono',
    WITHDRAWAL: 'Retiro',
  }
  return m[t] || t
}

const typeClass = (t: string) => {
  const m: Record<string, string> = {
    SELL_MXN: 'bg-info-light text-info-dark',
    BUY_MXN: 'bg-success-light text-success-dark',
    PAYMENT: 'bg-primary-light text-primary-dark',
    WITHDRAWAL: 'bg-warning-light text-warning-dark',
  }
  return m[t] || 'bg-active text-foreground'
}

function openCreateModal() {
  createForm.client_id = ''
  createForm.transaction_type = ''
  createForm.amount_mxn = 0
  createForm.amount_gtq = 0
  createForm.commission = 0
  createForm.exchange_rate = undefined
  createForm.notes = ''
  showCreateModal.value = true
}

async function handleCreate() {
  formLoading.value = true
  try {
    await createTransaction({
      client_id: createForm.client_id,
      transaction_type: createForm.transaction_type,
      amount_mxn: createForm.amount_mxn,
      amount_gtq: createForm.amount_gtq,
      commission: createForm.commission,
      exchange_rate: createForm.exchange_rate || undefined,
      notes: createForm.notes || undefined,
    })
    showCreateModal.value = false
  } catch { /* handled by composable */ } finally {
    formLoading.value = false
  }
}

function startVoid(txn: Transaction) {
  voidTarget.value = txn
  voidReason.value = ''
  showVoidModal.value = true
}

async function handleVoid() {
  if (!voidTarget.value) return
  formLoading.value = true
  try {
    await voidTransaction(voidTarget.value.id, voidReason.value)
    showVoidModal.value = false
  } catch { /* handled by composable */ } finally {
    formLoading.value = false
  }
}
</script>
