<script setup lang="ts">
import { dateFormat } from "@/lib/dateFormat";

defineProps<{
  name: string;
  date: string;
  description: string;
}>();
</script>

<template>
  <div class="flex items-start justify-between ps-5 border-s-2 border-border">
    <div class="relative pt-0 pb-6">
      <p class="-mt-1">{{ name }}</p>
      <p class="text-muted">{{ description }}</p>
      <div class="h-3 w-3 bg-muted rounded-full absolute top-0 start-[-27px] z-10"></div>
    </div>

    <p class="text-nowrap text-end">{{ dateFormat(new Date(date), "DD MMM YYYY") }}</p>
  </div>
</template>
