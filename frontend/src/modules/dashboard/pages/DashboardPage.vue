<template>
  <div class="dashboard-placeholder">
    <h1>Dashboard</h1>
    <p>Bienvenido, <strong>{{ user?.full_name }}</strong> ({{ user?.role }})</p>
    <p style="color: #94a3b8; margin-top: 0.5rem">
      Módulos disponibles próximamente — Fase 1 y 2 del proyecto.
    </p>
    <button @click="logout" style="margin-top: 1.5rem">Cerrar sesión</button>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/modules/auth/stores/authStore'
import { useAuth } from '@/modules/auth/composables/useAuth'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)
const { logout } = useAuth()

onMounted(async () => {
  if (!user.value) await authStore.fetchMe()
})
</script>

<style scoped>
.dashboard-placeholder {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #0f172a;
  color: #f8fafc;
}
</style>
