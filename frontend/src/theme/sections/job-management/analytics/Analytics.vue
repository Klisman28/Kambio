<script setup lang="ts">
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENT
import { Card } from "@/theme/components/ui/card";
// CUSTOM COMPONENT
import Icon from "@/theme/components/Icon.vue";
// CUSTOM COMPOSABLE
import { chartOptions } from "./useChartOptions";
// CUSTOM DATA
import { analytics } from "@/theme/data/dashboards/job-management";
</script>

<template>
  <div class="col-span-full md:col-span-6" v-for="item in analytics">
    <Card class="flex items-center justify-between h-full gap-6 px-6 py-2">
      <div>
        <p class="mb-1 text-sm font-medium text-muted">
          {{ item.title }}
        </p>
        <p class="text-2xl font-semibold">
          {{ item.amount }}
        </p>

        <div class="flex items-center gap-2 mt-3">
          <div class="grid w-5 h-5 rounded-full bg-primary/20 text-primary place-items-center">
            <Icon name="TrendingUp" :size="12" :strokeWidth="2" />
          </div>

          <p class="text-xs font-semibold text-primary">{{ item.increment }} Inc</p>
        </div>
      </div>

      <VueApexCharts
        width="100"
        height="160"
        type="radialBar"
        :series="[item.percent]"
        :options="chartOptions" />
    </Card>
  </div>
</template>
