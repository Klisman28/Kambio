<template>
  <div class="px-5 py-6 space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-foreground">Clientes</h1>
        <p class="text-sm text-muted-foreground">Listado general y gestión de clientes</p>
      </div>
      <Button @click="openCreateModal">+ Nuevo Cliente</Button>
    </div>

    <!-- Table -->
    <div class="bg-card border border-border rounded-xl shadow-sm overflow-hidden">
      <Table v-if="clients.length > 0">
        <TableHeader>
          <TableRow>
            <TableHead>Código</TableHead>
            <TableHead>Nombre</TableHead>
            <TableHead>Identificación</TableHead>
            <TableHead>Email / Tel</TableHead>
            <TableHead>Estado</TableHead>
            <TableHead class="text-right">Acciones</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="client in clients" :key="client.id">
            <TableCell class="font-mono text-xs text-primary">{{ client.code }}</TableCell>
            <TableCell class="font-medium">{{ client.full_name }}</TableCell>
            <TableCell class="text-muted-foreground">{{ client.id_number || '—' }}</TableCell>
            <TableCell>
              <div class="text-xs">{{ client.email || '—' }}</div>
              <div class="text-xs text-muted-foreground">{{ client.phone || '—' }}</div>
            </TableCell>
            <TableCell>
              <span v-if="client.is_active" class="px-2 py-1 text-[10px] uppercase font-bold text-success-dark bg-success-light rounded-full">Activo</span>
              <span v-else class="px-2 py-1 text-[10px] uppercase font-bold text-error-dark bg-error-light rounded-full">Inactivo</span>
            </TableCell>
            <TableCell class="text-right space-x-2">
              <Button size="sm" variant="outline" @click="openEditModal(client)">Editar</Button>
              <Button size="sm" variant="default" @click="$router.push(`/clients/${client.id}`)">Detalle</Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
      
      <div v-if="loading" class="p-6 text-center text-muted-foreground">Cargando clientes...</div>
      <div v-if="!loading && clients.length === 0" class="p-6 text-center text-muted-foreground">No hay clientes registrados.</div>
    </div>

    <!-- Modal Form (Create / Edit) -->
    <div v-if="isModalOpen" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-card w-full max-w-md rounded-xl shadow-xl overflow-hidden border border-border flex flex-col max-h-full">
        <div class="px-6 py-4 border-b border-border flex justify-between items-center">
          <h3 class="text-lg font-bold">{{ isEditing ? 'Editar Cliente' : 'Nuevo Cliente' }}</h3>
          <button @click="closeModal" class="text-muted-foreground hover:text-foreground">&times;</button>
        </div>
        
        <div class="p-6 overflow-y-auto">
          <form @submit.prevent="submitForm" class="space-y-4">
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-muted-foreground">Nombre / Razón Social *</label>
              <input v-model="form.full_name" required class="w-full h-10 px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
            </div>
            
            <div class="flex flex-col gap-1.5">
              <label class="text-sm font-medium text-muted-foreground">Identificación (NIT, DPI)</label>
              <input v-model="form.id_number" class="w-full h-10 px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="flex flex-col gap-1.5">
                <label class="text-sm font-medium text-muted-foreground">Correo electrónico</label>
                <input v-model="form.email" type="email" class="w-full h-10 px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
              </div>
              <div class="flex flex-col gap-1.5">
                <label class="text-sm font-medium text-muted-foreground">Teléfono</label>
                <input v-model="form.phone" class="w-full h-10 px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
              </div>
            </div>
            
            <div class="flex items-center gap-2 mt-2">
              <input type="checkbox" id="isActive" v-model="form.is_active" class="rounded border-border text-primary focus:ring-primary" />
              <label for="isActive" class="text-sm font-medium text-muted-foreground">Cliente Activo</label>
            </div>

            <div class="flex justify-end gap-3 mt-6">
              <Button type="button" variant="outline" @click="closeModal" :disabled="formLoading">Cancelar</Button>
              <Button type="submit" :disabled="formLoading">{{ isEditing ? 'Actualizar' : 'Guardar' }}</Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useClients, type Client } from '@/modules/clients/composables/useClients'
import { Button } from '@/theme/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/theme/components/ui/table'

const { clients, loading, loadClients, createClient, updateClient } = useClients()
const router = useRouter()

// Modal State
const isModalOpen = ref(false)
const isEditing = ref(false)
const formLoading = ref(false)
const currentClientId = ref<string | null>(null)

const form = reactive({
  full_name: '',
  id_number: '',
  email: '',
  phone: '',
  is_active: true
})

onMounted(() => {
  loadClients()
})

const resetForm = () => {
  form.full_name = ''
  form.id_number = ''
  form.email = ''
  form.phone = ''
  form.is_active = true
  currentClientId.value = null
  isEditing.value = false
}

const openCreateModal = () => {
  resetForm()
  isModalOpen.value = true
}

const openEditModal = (client: Client) => {
  resetForm()
  isEditing.value = true
  currentClientId.value = client.id
  form.full_name = client.full_name
  form.id_number = client.id_number || ''
  form.email = client.email || ''
  form.phone = client.phone || ''
  form.is_active = client.is_active
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const submitForm = async () => {
  formLoading.value = true
  try {
    const payload = {
      full_name: form.full_name,
      id_number: form.id_number || undefined,
      email: form.email || undefined,
      phone: form.phone || undefined,
      is_active: form.is_active
    }

    if (isEditing.value && currentClientId.value) {
      await updateClient(currentClientId.value, payload)
    } else {
      await createClient(payload)
    }
    closeModal()
  } catch (e) {
    // Errors are handled by composable pushing to notivue
  } finally {
    formLoading.value = false
  }
}
</script>
