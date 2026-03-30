<script setup lang="ts">
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";

defineProps<{ title: string; description: string; id: string }>();
</script>

<template>
  <div class="flex items-center justify-between p-4 space-x-2 border rounded-lg border-border">
    <Label :for="id" class="cursor-pointer">
      {{ title }}
      <p class="mt-1 text-xs font-normal text-muted">{{ description }}</p>
    </Label>

    <Switch :id="id" />
  </div>
</template>
