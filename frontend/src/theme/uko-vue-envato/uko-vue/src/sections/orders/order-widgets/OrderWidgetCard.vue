<script setup lang="ts">
import { Card, CardTitle } from "@/components/ui/card";

// ==============================================================
interface Props {
  title: string;
  description: string;
}
// ==============================================================

defineProps<Props>();
</script>

<template>
  <Card class="p-5 text-center col-span-full 2xl:col-span-2 lg:col-span-4 sm:col-span-6">
    <CardTitle class="mb-3">{{ title }}</CardTitle>
    <p class="text-xs font-medium uppercase text-muted">{{ description }}</p>
  </Card>
</template>
