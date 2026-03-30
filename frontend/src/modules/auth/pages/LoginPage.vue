<template>
  <!--
    LoginPage.vue — Kambio
    Este componente usa el layout y estilos del tema comprado.
    Cuando el tema esté disponible en src/theme/, reemplaza el
    wrapper por el componente de layout correspondiente del tema.
  -->
  <div class="login-wrapper">
    <div class="login-card">
      <div class="login-header">
        <h1>Kambio</h1>
        <p>Sistema financiero MXN · GTQ</p>
      </div>

      <form @submit.prevent="handleSubmit" class="login-form">
        <div class="field">
          <label for="email">Correo electrónico</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="admin@kambio.dev"
            autocomplete="username"
            required
          />
        </div>

        <div class="field">
          <label for="password">Contraseña</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            autocomplete="current-password"
            required
          />
        </div>

        <p v-if="error" class="error-message">{{ error }}</p>

        <button type="submit" :disabled="loading" class="btn-login">
          {{ loading ? 'Ingresando…' : 'Ingresar' }}
        </button>
      </form>
    </div>
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

<style scoped>
/* Estilos mínimos temporales — serán reemplazados al integrar el tema comprado */
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f172a;
}
.login-card {
  background: #1e293b;
  border-radius: 12px;
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
}
.login-header {
  text-align: center;
  margin-bottom: 2rem;
  color: #f8fafc;
}
.login-header h1 {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}
.login-header p {
  color: #94a3b8;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1.25rem;
}
.field label {
  color: #cbd5e1;
  font-size: 0.875rem;
  font-weight: 500;
}
.field input {
  padding: 0.6rem 0.875rem;
  border-radius: 8px;
  border: 1px solid #334155;
  background: #0f172a;
  color: #f8fafc;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}
.field input:focus {
  border-color: #6366f1;
}
.btn-login {
  width: 100%;
  padding: 0.7rem;
  border-radius: 8px;
  border: none;
  background: #6366f1;
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-login:hover:not(:disabled) {
  background: #4f46e5;
}
.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.error-message {
  color: #f87171;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}
</style>
