<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardContent } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";

// ===========================
interface Props {
  color: string;
  title: string;
  iconName: string;
  description: string;
}
// ===========================

defineProps<Props>();
</script>

<template>
  <Card class="p-5 xl:p-6">
    <CardContent>
      <div
        class="inline-block p-4 mb-5 rounded-lg"
        :class="{
          'bg-info/10 text-info': color === 'info',
          'bg-error/10 text-error': color === 'error',
          'bg-warning/10 text-warning': color === 'warning',
          'bg-primary/10 text-primary': color === 'primary',
          'bg-success/10 text-primary': color === 'success'
        }">
        <Icon :name="iconName" :size="24" class="w-6 h-6" />
      </div>

      <h5 class="mb-2 text-sm font-semibold">{{ title }}</h5>
      <p class="font-normal text-small text-muted">
        {{ description }}
      </p>
    </CardContent>
  </Card>
</template>
