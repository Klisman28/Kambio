<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPOSABLE
import { useApexChartOptions } from "@/theme/hooks/useApexChartOptions";

const series = ref([50, 30, 20]);

const chartOptions = useApexChartOptions({
  stroke: { show: false },
  colors: ["#2499EF", "#FFC675", "#738499"],
  labels: ["Transactions", "Payouts", "Sales"],
  legend: {
    fontWeight: 500,
    position: "bottom",
    horizontalAlign: "center",
    itemMargin: { horizontal: 10, vertical: 0 },
    onItemClick: { toggleDataSeries: false },
    onItemHover: { highlightDataSeries: false },
    markers: { offsetX: -5, size: 6, shape: "circle" }
  }
});
</script>

<template>
  <Card class="py-6 col-span-full lg:col-span-4 self-start">
    <CardTitle class="px-5 mb-6 text-center">Project Status</CardTitle>
    <VueApexCharts type="donut" :options="chartOptions" :series="series" height="340" />
  </Card>
</template>
