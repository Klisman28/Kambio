import { ref } from 'vue'
import http from '@/services/http'

export interface RecentTransaction {
  id: string
  code: string
  client_name: string
  transaction_type: string
  amount_mxn: number
  amount_gtq: number
  commission: number
  status: string
}

export interface CashSummary {
  is_open: boolean
  opening_mxn: number
  opening_gtq: number
}

export interface DashboardSummary {
  active_clients: number
  transactions_today: number
  commission_today: number
  cash: CashSummary
  recent_transactions: RecentTransaction[]
}

const TRANSACTION_TYPE_LABELS: Record<string, string> = {
  SELL_MXN: 'Venta MXN',
  BUY_MXN: 'Compra MXN',
  PAYMENT: 'Abono',
  WITHDRAWAL: 'Retiro',
}

export function useTransactionTypeLabel(type: string): string {
  return TRANSACTION_TYPE_LABELS[type] ?? type
}

export function useDashboard() {
  const summary = ref<DashboardSummary | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadSummary() {
    loading.value = true
    error.value = null
    try {
      const { data } = await http.get<DashboardSummary>('/api/v1/dashboard/summary')
      summary.value = data
    } catch {
      error.value = 'No se pudo cargar el resumen del dashboard'
    } finally {
      loading.value = false
    }
  }

  return { summary, loading, error, loadSummary }
}
