<script setup lang="ts">
defineProps<{ title: string }>();
</script>

<template>
  <div class="space-y-6">
    <h5 class="text-sm font-semibold leading-none">{{ title }}</h5>

    <div class="grid gap-6 xl:grid-cols-2">
      <slot></slot>
    </div>
  </div>
</template>
