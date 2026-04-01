<template>
  <div class="w-full max-w-md mx-auto">
    <h3 class="font-semibold text-2xl text-foreground">Sign In</h3>
    <div class="flex gap-1 mt-1 mb-10 text-sm font-medium">
      <p class="text-muted">Acceso seguro al sistema Kambio.</p>
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="space-y-5">
        <div class="flex flex-col gap-1.5">
          <label for="email" class="text-sm font-medium text-muted">Correo electrónico</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="admin@kambio.dev"
            autocomplete="username"
            required
            class="w-full h-10 px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground placeholder:text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:opacity-50 transition-colors"
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
            class="w-full h-10 px-3 py-2 text-sm bg-transparent border rounded-md border-border text-foreground placeholder:text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:opacity-50 transition-colors"
          />
        </div>
      </div>

      <p v-if="error" class="text-sm font-medium text-error mt-4">{{ error }}</p>

      <Button :disabled="loading" type="submit" class="mt-8! w-full">
        {{ loading ? 'Ingresando…' : 'Ingresar' }}
      </Button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuth } from '@/modules/auth/composables/useAuth'
import { Button } from '@/theme/components/ui/button'

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
