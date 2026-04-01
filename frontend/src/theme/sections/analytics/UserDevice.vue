<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
// CUSTOM DATA
import { userDevices } from "@/theme/data/dashboards/analytics";
</script>

<template>
  <Card class="p-6 col-span-full lg:col-span-4">
    <CardTitle class="mb-6">User Device</CardTitle>

    <CardContent class="space-y-5">
      <div
        :key="device.id"
        v-for="device in userDevices"
        class="flex items-center justify-between gap-2 p-4 rounded-lg bg-gray-50 dark:bg-gray-700/10">
        <div class="flex items-center gap-2">
          <Icon :name="device.icon" class="text-primary" />
          <p>{{ device.deviceName }}</p>
        </div>

        <p class="font-semibold">{{ device.value }}</p>
      </div>
    </CardContent>
  </Card>
</template>
