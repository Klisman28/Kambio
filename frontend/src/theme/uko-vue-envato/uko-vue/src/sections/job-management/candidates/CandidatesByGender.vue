<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/components/ui/card";
// CUSTOM COMPOSABLE
import { useApexChartOptions } from "@/hooks/useApexChartOptions";

const series = ref([65, 35]);

const chartOptions = useApexChartOptions({
  labels: ["Male", "Female"],
  colors: ["#7EC9FF", "#45ABF6"],
  stroke: { show: false },
  legend: {
    offsetY: 5,
    offsetX: 0,
    position: "bottom",
    horizontalAlign: "center",
    itemMargin: { horizontal: 10, vertical: 0 },
    markers: { offsetX: -5, size: 6, shape: "circle" }
  },
  responsive: [
    { breakpoint: 1300, options: { chart: { height: 360 } } },
    { breakpoint: 1100, options: { chart: { height: 460 } } }
  ]
});
</script>

<template>
  <Card class="p-6 col-span-full 2xl:col-span-4 xl:col-span-5 lg:col-span-5 self-start">
    <CardTitle class="mb-5 text-center">Candidates by Gender</CardTitle>
    <VueApexCharts type="pie" :options="chartOptions" :series="series" height="310" />
  </Card>
</template>
