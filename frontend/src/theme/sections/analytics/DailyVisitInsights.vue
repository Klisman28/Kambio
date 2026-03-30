<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/components/ui/card";
// CUSTOM COMPOSABLE
import { useApexChartOptions } from "@/hooks/useApexChartOptions";

const chartOptions = useApexChartOptions({
  yaxis: { show: false },
  colors: ["#7EC9FF", "#E5F3FD"],
  stroke: { show: true, width: 2, colors: ["transparent"] },
  plotOptions: {
    bar: { horizontal: false, borderRadius: 5, columnWidth: "40%" }
  },
  xaxis: {
    categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    labels: { style: { fontWeight: 500, colors: "#738499" } }
  },
  legend: {
    show: true,
    offsetX: -15,
    position: "top",
    fontWeight: 500,
    horizontalAlign: "left",
    itemMargin: { horizontal: 10, vertical: 0 },
    markers: { offsetX: -5, offsetY: 1, size: 6, shape: "circle" }
  },
  responsive: [
    {
      breakpoint: 1024,
      options: { plotOptions: { bar: { columnWidth: "30%", borderRadius: 10 } } }
    },
    {
      breakpoint: 800,
      options: { plotOptions: { bar: { columnWidth: "30%", borderRadius: 7 } } }
    },
    {
      breakpoint: 600,
      options: { plotOptions: { bar: { columnWidth: "40%", borderRadius: 5 } } }
    },
    {
      breakpoint: 400,
      options: { plotOptions: { bar: { columnWidth: "50%", borderRadius: 5 } } }
    }
  ]
});

const series = ref([
  { name: "Desktop", data: [90, 60, 70, 75, 60, 70] },
  { name: "Mobile", data: [70, 90, 50, 30, 70, 60] }
]);
</script>

<template>
  <Card class="pt-6 col-span-full lg:col-span-4">
    <CardTitle class="px-6 mb-4">Daily Visit Insights</CardTitle>
    <VueApexCharts type="bar" height="290" :options="chartOptions" :series="series" />
  </Card>
</template>
