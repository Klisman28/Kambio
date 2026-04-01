<template>
  <div class="grid min-h-screen lg:grid-cols-2 bg-primary">
    <!-- Branding Side -->
    <div class="hidden items-center p-20 text-white lg:flex xl:px-40">
      <div>
        <h1 class="mb-4 text-5xl font-bold tracking-tight text-white">Kambio</h1>
        <h5 class="text-xl font-semibold text-primary-light">Sistema financiero MXN · GTQ</h5>
        <p class="mt-4 text-sm leading-relaxed text-white/80">
          Control de divisas, libro mayor por cliente, y operaciones rápidas de caja.
          Acceso exclusivo para personal autorizado.
        </p>
      </div>
    </div>

    <!-- Form Side -->
    <div
      class="content-center col-span-full p-10 sm:px-16 sm:py-20 bg-background lg:rounded-tl-[2rem] lg:rounded-bl-[2rem] md:px-40 lg:px-20 2xl:px-52 lg:col-span-1 lg:rtl:rounded-tr-[2rem] lg:rtl:rounded-br-[2rem] rtl:rounded-tl-none rtl:rounded-bl-none">
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
// AuthLayout para Kambio
</script>
