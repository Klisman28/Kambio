<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/components/ui/card";
// CUSTOM COMPOSABLE
import { useOrderAnalytics } from "./hooks/useOrderAnalytics";
import { useApexChartOptions } from "@/hooks/useApexChartOptions";

const { isLoading, orderAnalytics } = useOrderAnalytics();

const chartOptions = useApexChartOptions({
  colors: ["#2499EF"],
  plotOptions: {
    bar: { borderRadius: 5, columnWidth: "25%" }
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
    labels: { style: { colors: "#738499", fontSize: "12px", fontWeight: 500 } }
  },
  yaxis: {
    min: 0,
    stepSize: 5000,
    tickAmount: 4,
    labels: {
      formatter: (value) => (value > 0 ? value / 1000 + "K" : value.toString()),
      style: { fontWeight: 600, colors: "#738499", fontSize: "11px" }
    }
  },

  responsive: [
    {
      breakpoint: 576,
      options: {
        chart: { height: 400 },
        plotOptions: {
          bar: { horizontal: true, borderRadius: 7 }
        },
        xaxis: {
          labels: {
            show: false
          }
        }
      }
    }
  ]
});

const series = ref([{ name: "Orders", data: orderAnalytics || [] }]);
</script>

<template>
  <Card>
    <CardTitle class="px-5 pt-6 pb-3">Order Overview</CardTitle>

    <!-- SHOW LOADING SKELETON -->
    <div class="px-5 pt-1 pb-5 space-y-3 animate-pulse" v-if="isLoading">
      <div v-for="i in 11" :key="i" class="w-full h-3 rounded-md bg-skeleton"></div>
    </div>

    <!-- SHOW VIEW WHEN DATA IS LOADED -->
    <div class="pl-2 pr-4 sm:pb-2" v-if="!isLoading && orderAnalytics">
      <VueApexCharts type="bar" height="250" :options="chartOptions" :series="series" />
    </div>
  </Card>
</template>
