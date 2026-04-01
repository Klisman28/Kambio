import { ref } from 'vue'
import http from '@/services/http'
import { push } from 'notivue'

export interface CashSession {
  id: string
  status: 'OPEN' | 'CLOSED'
  opening_amount_mxn: string
  opening_amount_gtq: string
  closing_amount_mxn?: string
  closing_amount_gtq?: string
  difference_mxn?: string
  difference_gtq?: string
  opened_by: string
  closed_by?: string
  opened_at: string
  closed_at?: string
  notes?: string
}

export function useCash() {
  const currentSession = ref<CashSession | null>(null)
  const loading = ref(false)
  const noSession = ref(false)

  async function fetchCurrent() {
    loading.value = true
    noSession.value = false
    try {
      const { data } = await http.get('/api/v1/cash/current')
      currentSession.value = data
    } catch (error: any) {
      if (error.response?.status === 404) {
        currentSession.value = null
        noSession.value = true
      } else {
        push.error('Error al consultar la caja')
      }
    } finally {
      loading.value = false
    }
  }

  async function openCash(payload: {
    opening_amount_mxn: number
    opening_amount_gtq: number
    notes?: string
  }) {
    loading.value = true
    try {
      const { data } = await http.post('/api/v1/cash/open', payload)
      currentSession.value = data
      push.success('Caja abierta correctamente')
      return data
    } catch (error: any) {
      push.error(error.response?.data?.detail || 'Error al abrir caja')
      throw error
    } finally {
      loading.value = false
    }
  }

  async function closeCash(sessionId: string, payload: {
    closing_amount_mxn: number
    closing_amount_gtq: number
    notes?: string
  }) {
    loading.value = true
    try {
      const { data } = await http.post(`/api/v1/cash/${sessionId}/close`, payload)
      currentSession.value = data
      push.success('Caja cerrada correctamente')
      return data
    } catch (error: any) {
      push.error(error.response?.data?.detail || 'Error al cerrar caja')
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    currentSession,
    loading,
    noSession,
    fetchCurrent,
    openCash,
    closeCash,
  }
}
