<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPOSABLE
import { useApexChartOptions } from "@/theme/hooks/useApexChartOptions";

const chartOptions = useApexChartOptions({
  grid: { show: true },
  colors: ["#2499EF"],
  plotOptions: {
    bar: {
      borderRadius: 10,
      columnWidth: "35%",
      borderRadiusApplication: "end"
    }
  },
  xaxis: {
    crosshairs: { show: false },
    categories: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec"
    ],
    labels: {
      style: {
        colors: "#738499",
        fontSize: "12px",
        fontWeight: 500
      }
    }
  },
  yaxis: {
    min: 0,
    stepSize: 5000,
    tickAmount: 4,
    labels: {
      formatter: (value) => (value > 0 ? value / 1000 + "K" : value.toString()),
      style: {
        fontWeight: 600,
        colors: "#738499",
        fontSize: "11px"
      }
    }
  },
  responsive: [
    {
      breakpoint: 576,
      options: {
        chart: { height: 300 },
        plotOptions: { bar: { horizontal: true, borderRadius: 7 } },
        xaxis: {
          min: 0,
          tickAmount: 4,
          stepSize: 5000,
          labels: {
            formatter: (value: number) => (value > 0 ? value / 1000 + "K" : value.toString()),
            style: { fontWeight: 600 }
          }
        }
      }
    }
  ]
});

const series = ref([
  {
    name: "Spent",
    data: [15000, 5000, 12000, 5500, 7500, 15000, 3000, 15000, 13000, 14000, 4000, 15000]
  }
]);
</script>

<template>
  <Card class="pt-6 col-span-full xl:col-span-8 self-start">
    <CardTitle class="px-5 mb-4">Total Spent</CardTitle>

    <div class="pl-2 pr-3 sm:pr-0">
      <VueApexCharts type="bar" height="300" :options="chartOptions" :series="series" />
    </div>
  </Card>
</template>
