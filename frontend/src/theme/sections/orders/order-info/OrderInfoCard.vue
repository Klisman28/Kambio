<script setup lang="ts">
// SHADCN COMPONENTS
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";

// ==============================================================
interface Props {
  icon: string;
  title: string;
  heading: string;
  iconColor: "default" | "destructive" | "success" | "warning";
}
// ==============================================================

defineProps<Props>();
</script>

<template>
  <Card class="p-5 col-span-full 2xl:col-span-3 sm:col-span-6">
    <CardHeader class="flex-row justify-between">
      <CardTitle>{{ heading }}</CardTitle>

      <Badge class="justify-center w-10 h-10" :variant="iconColor">
        <Icon :name="icon" :size="20" :stroke-width="2" />
      </Badge>
    </CardHeader>

    <div>
      <h5 class="mb-2 text-sm font-medium">
        {{ title }}
      </h5>

      <p class="text-xs font-medium text-muted">
        <slot></slot>
      </p>
    </div>
  </Card>
</template>
