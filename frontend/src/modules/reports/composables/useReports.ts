import { ref } from 'vue'
import http from '@/services/http'
import { push } from 'notivue'
import type { CashSession } from '@/modules/cash/composables/useCash'
import type { Transaction } from '@/modules/transactions/composables/useTransactions'

export interface TransactionReportSummary {
  total_transactions: number
  total_commission: string
  total_amount_mxn: string
  total_amount_gtq: string
}

export interface TransactionReport {
  summary: TransactionReportSummary
  transactions: Transaction[]
}

export interface CashReportSummary {
  total_sessions: number
  total_difference_mxn: string
  total_difference_gtq: string
}

export interface CashReport {
  summary: CashReportSummary
  sessions: CashSession[]
}

export function useReports() {
  const loading = ref(false)
  
  const transactionReport = ref<TransactionReport | null>(null)
  const cashReport = ref<CashReport | null>(null)

  async function loadTransactionReport(startDate: string, endDate: string) {
    loading.value = true
    try {
      const { data } = await http.get('/api/v1/reports/transactions', {
        params: { start_date: startDate, end_date: endDate }
      })
      transactionReport.value = data
      return data
    } catch (error) {
      push.error('Error al generar reporte de transacciones')
    } finally {
      loading.value = false
    }
  }

  async function loadCashReport(startDate: string, endDate: string) {
    loading.value = true
    try {
      const { data } = await http.get('/api/v1/reports/cash-summary', {
        params: { start_date: startDate, end_date: endDate }
      })
      cashReport.value = data
      return data
    } catch (error) {
      push.error('Error al generar resumen de cajas')
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    transactionReport,
    cashReport,
    loadTransactionReport,
    loadCashReport
  }
}
