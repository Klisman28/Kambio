<script setup lang="ts">
import { ref, watchEffect } from "vue";
// SHADCN COMPONENTS
import { Progress } from "@/components/ui/progress";

// ==============================================================
interface Props {
  title: string;
  value: number;
}
// ==============================================================

const progress = ref(0);
const props = defineProps<Props>();

watchEffect((cleanupFn) => {
  const timer = setTimeout(() => (progress.value = props.value), 300);
  cleanupFn(() => clearTimeout(timer));
});
</script>

<template>
  <div class="flex flex-wrap items-center justify-between gap-6">
    <div class="flex items-center gap-2 min-w-28">
      <div class="w-2 h-2 rounded-full bg-primary"></div>
      <p class="text-sm font-medium">
        {{ title }}
      </p>
    </div>

    <div class="grow">
      <Progress :model-value="progress" class="w-full h-2"></Progress>
    </div>

    <p class="text-[12px] font-semibold min-w-10 text-right">{{ value }}%</p>
  </div>
</template>
