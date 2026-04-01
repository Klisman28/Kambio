<script setup lang="ts">
// SHADCN COMPONENT
import { Card } from "@/theme/components/ui/card";
// CUSTOM COMPONENT
import Icon from "@/theme/components/Icon.vue";
// DATA LIST
import { widgets } from "@/theme/data/dashboards/sass";
</script>

<template>
  <div class="grid grid-cols-4 col-span-full gap-7">
    <Card class="p-6 col-span-full sm:col-span-2 xl:col-span-1" v-for="item in widgets">
      <div class="flex items-center gap-4">
        <div
          class="grid w-12 h-12 rounded-lg place-items-center"
          :class="{
            'bg-info/10 text-info': item.color === 'info',
            'bg-error/10 text-error': item.color === 'error',
            'bg-warning/10 text-warning': item.color === 'warning',
            'bg-primary/10 text-primary': item.color === 'primary'
          }">
          <Icon :name="item.icon" />
        </div>

        <div>
          <p class="mb-1 text-sm font-medium truncate text-muted">
            {{ item.title }}
          </p>

          <p class="text-xl font-bold">{{ item.amount }}</p>
        </div>
      </div>
    </Card>
  </div>
</template>
