<script setup lang="ts">
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";

defineProps<{ label: string; id: string }>();
</script>

<template>
  <div class="flex items-center justify-between p-4 space-x-2 cursor-pointer">
    <Label :for="id">{{ label }}</Label>
    <Switch :id="id" />
  </div>
</template>
