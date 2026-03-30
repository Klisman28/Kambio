import { ref } from 'vue'
import http from '@/services/http'
import { push } from 'notivue'

export interface Client {
  id: string
  code: string
  full_name: string
  phone?: string
  email?: string
  is_active: boolean
  id_number?: string
}

export function useClients() {
  const clients = ref<Client[]>([])
  const loading = ref(false)

  async function loadClients() {
    loading.value = true
    try {
      const { data } = await http.get('/api/v1/clients')
      clients.value = data
    } catch (error) {
      push.error('Error al cargar clientes')
    } finally {
      loading.value = false
    }
  }

  async function createClient(payload: Partial<Client>) {
    loading.value = true
    try {
      const { data } = await http.post('/api/v1/clients', payload)
      push.success('Cliente creado correctamente')
      await loadClients()
      return data
    } catch (error: any) {
      push.error(error.response?.data?.detail || 'Error al crear cliente')
      throw error
    } finally {
      loading.value = false
    }
  }

  async function updateClient(id: string, payload: Partial<Client>) {
    loading.value = true
    try {
      const { data } = await http.patch(`/api/v1/clients/${id}`, payload)
      push.success('Cliente actualizado correctamente')
      await loadClients()
      return data
    } catch (error: any) {
      push.error(error.response?.data?.detail || 'Error al actualizar cliente')
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    clients,
    loading,
    loadClients,
    createClient,
    updateClient
  }
}
