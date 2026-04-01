<script setup lang="ts">
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPOSABLE
import { useChartOptions } from "./useChartOptions";

const { chartOptions, series } = useChartOptions();
</script>

<template>
  <Card class="px-5 pt-6 col-span-full xl:col-span-4">
    <CardTitle>Study Time Last Week</CardTitle>
    <VueApexCharts type="bar" height="280" :options="chartOptions" :series="series" />
  </Card>
</template>
