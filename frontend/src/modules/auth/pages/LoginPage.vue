<template>
  <div class="w-full max-w-md mx-auto">
    <h3 class="mb-2 text-2xl font-bold text-foreground">Sign In</h3>
    <div class="flex gap-1 mt-1 mb-8 text-sm font-medium">
      <p class="text-muted">Acceso seguro al sistema Kambio.</p>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-5">
      <div class="flex flex-col gap-1.5">
        <label for="email" class="text-sm font-medium text-muted">Correo electrónico</label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          placeholder="admin@kambio.dev"
          autocomplete="username"
          required
          class="w-full h-10 px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
        />
      </div>

      <div class="flex flex-col gap-1.5">
        <label for="password" class="text-sm font-medium text-muted">Contraseña</label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          autocomplete="current-password"
          required
          class="w-full h-10 px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
        />
      </div>

      <p v-if="error" class="text-sm font-medium text-error">{{ error }}</p>

      <button
        type="submit"
        :disabled="loading"
        class="inline-flex items-center justify-center w-full h-10 px-4 py-2 mt-4 text-sm font-medium text-white transition-colors rounded-md bg-primary hover:bg-primary-dark focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
      >
        {{ loading ? 'Ingresando…' : 'Ingresar' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuth } from '@/modules/auth/composables/useAuth'

const { login } = useAuth()

const form = reactive({ email: '', password: '' })
const loading = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  loading.value = true
  error.value = null
  try {
    await login(form.email, form.password)
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>
