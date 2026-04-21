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

export interface DailyDataPoint {
  date: string
  count: number
  amount_mxn: string
  amount_gtq: string
  commission: string
}

export interface TypeDistributionItem {
  transaction_type: string
  count: number
  total_mxn: string
  total_gtq: string
  total_commission: string
}

export interface TransactionAnalytics {
  start_date: string
  end_date: string
  daily_series: DailyDataPoint[]
  type_distribution: TypeDistributionItem[]
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
  const transactionAnalytics = ref<TransactionAnalytics | null>(null)
  const cashReport = ref<CashReport | null>(null)

  async function loadTransactionReport(startDate: string, endDate: string) {
    loading.value = true
    try {
      const [{ data: reportData }, { data: analyticsData }] = await Promise.all([
        http.get('/api/v1/reports/transactions', { params: { start_date: startDate, end_date: endDate } }),
        http.get('/api/v1/reports/transactions/analytics', { params: { start_date: startDate, end_date: endDate } })
      ])
      transactionReport.value = reportData
      transactionAnalytics.value = analyticsData
      return reportData
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
    transactionAnalytics,
    cashReport,
    loadTransactionReport,
    loadCashReport
  }
}
