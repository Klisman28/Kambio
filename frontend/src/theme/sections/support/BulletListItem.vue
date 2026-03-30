<script setup lang="ts">
defineProps<{ item: string }>();
</script>

<template>
  <li class="flex items-center gap-3">
    <div class="h-2.5 w-2.5 bg-slate-300 dark:bg-slate-700 rounded-full"></div>
    {{ item }}
  </li>
</template>
