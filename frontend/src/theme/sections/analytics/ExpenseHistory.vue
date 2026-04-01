<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPOSABLE
import { useApexChartOptions } from "@/theme/hooks/useApexChartOptions";

const chartOptions = useApexChartOptions({
  colors: ["#2499EF"],
  grid: { show: true },
  stroke: { curve: "smooth" },
  xaxis: {
    type: "datetime",
    categories: [
      "01/01/2011 GMT",
      "01/02/2011 GMT",
      "01/03/2011 GMT",
      "01/04/2011 GMT",
      "01/05/2011 GMT",
      "01/06/2011 GMT",
      "01/07/2011 GMT"
    ],
    labels: {
      format: "ddd",
      style: {
        colors: "#738499",
        fontSize: "12px",
        fontWeight: 500
      }
    },
    axisBorder: { show: false },
    axisTicks: { show: false },
    tooltip: { enabled: false }
  },
  yaxis: {
    min: 1000,
    show: true,
    tickAmount: 5,
    labels: {
      formatter: (value) => value / 1000 + "K",
      style: {
        fontSize: "12px",
        fontWeight: 500,
        colors: "#738499"
      }
    }
  }
});

const series = ref([{ name: "Expense", data: [10000, 5000, 23000, 20000, 28000, 30000, 50000] }]);
</script>

<template>
  <Card class="pt-6 pb-2 col-span-full lg:col-span-8 self-start">
    <CardTitle class="px-6 mb-4">Expense History</CardTitle>

    <div class="pl-3 pr-5">
      <VueApexCharts type="area" height="290" :options="chartOptions" :series="series" />
    </div>
  </Card>
</template>
