import { ref } from 'vue'
import http from '@/services/http'
import { push } from 'notivue'

export interface Transaction {
  id: string
  code: string
  client_id: string
  cash_session_id: string
  transaction_type: 'SELL_MXN' | 'BUY_MXN' | 'PAYMENT' | 'WITHDRAWAL'
  amount_mxn: string
  amount_gtq: string
  commission: string
  exchange_rate?: string
  status: 'ACTIVE' | 'VOIDED'
  voided_by?: string
  voided_at?: string
  void_reason?: string
  void_of_id?: string
  created_by: string
  created_at: string
  notes?: string
}

export function useTransactions() {
  const transactions = ref<Transaction[]>([])
  const loading = ref(false)

  async function loadTransactions(status?: string) {
    loading.value = true
    try {
      const params: Record<string, any> = { limit: 100 }
      if (status) params.status = status
      const { data } = await http.get('/api/v1/transactions', { params })
      transactions.value = data
    } catch (error) {
      push.error('Error al cargar transacciones')
    } finally {
      loading.value = false
    }
  }

  async function createTransaction(payload: {
    client_id: string
    transaction_type: string
    amount_mxn: number
    amount_gtq: number
    commission: number
    exchange_rate?: number
    notes?: string
  }) {
    loading.value = true
    try {
      const { data } = await http.post('/api/v1/transactions', payload)
      push.success(`Transacción ${data.code} registrada`)
      await loadTransactions()
      return data
    } catch (error: any) {
      const detail = error.response?.data?.detail
      if (typeof detail === 'string') {
        push.error(detail)
      } else if (Array.isArray(detail)) {
        push.error(detail.map((e: any) => e.msg).join(', '))
      } else {
        push.error('Error al crear transacción')
      }
      throw error
    } finally {
      loading.value = false
    }
  }

  async function voidTransaction(txnId: string, reason: string) {
    loading.value = true
    try {
      const { data } = await http.post(`/api/v1/transactions/${txnId}/void`, {
        void_reason: reason,
      })
      push.success(`Transacción ${data.code} anulada`)
      await loadTransactions()
      return data
    } catch (error: any) {
      push.error(error.response?.data?.detail || 'Error al anular transacción')
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    transactions,
    loading,
    loadTransactions,
    createTransaction,
    voidTransaction,
  }
}
