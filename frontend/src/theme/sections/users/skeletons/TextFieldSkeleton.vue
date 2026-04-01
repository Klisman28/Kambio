<script setup lang="ts">
import { Label } from "@/theme/components/ui/label";
defineProps<{ label?: string }>();
</script>

<template>
  <div>
    <Label v-if="label" class="inline-block mb-3 text-sm font-medium">{{ label }}</Label>
    <div class="rounded-md h-11 bg-skeleton animate-pulse"></div>
  </div>
</template>
