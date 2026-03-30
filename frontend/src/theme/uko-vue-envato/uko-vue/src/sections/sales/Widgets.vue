<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardContent } from "@/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
// DATA LIST
import { widgets } from "@/data/dashboards/sales";
</script>

<template>
  <div class="grid grid-cols-12 gap-7 col-span-full xl:col-span-6">
    <Card class="px-6 py-6 col-span-full md:col-span-6 lg:col-span-6" v-for="widget in widgets">
      <CardContent class="flex items-center justify-between gap-6">
        <div>
          <p class="mb-1 text-sm font-medium text-muted">
            {{ widget.title }}
          </p>

          <p class="text-xl font-bold">
            {{ widget.amount }}
          </p>

          <div class="flex items-center gap-2 mt-4">
            <div
              class="grid w-6 h-6 rounded-full place-items-center"
              :class="{
                'bg-success/10 text-success': widget.isUp,
                'bg-error/10 text-error': !widget.isUp
              }">
              <Icon
                :size="14"
                :strokeWidth="2"
                :name="widget.isUp ? 'TrendingUp' : 'TrendingDown'" />
            </div>

            <p
              class="text-sm font-semibold"
              :class="{ 'text-success': widget.isUp, 'text-error': !widget.isUp }">
              +10.23%
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
