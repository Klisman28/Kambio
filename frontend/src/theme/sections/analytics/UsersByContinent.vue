<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// CUSTOM COMPOSABLE
import { useApexChartOptions } from "@/theme/hooks/useApexChartOptions";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// CUSTOM DATA
import { usersByContinent } from "@/theme/data/dashboards/analytics";

const chartOptions = useApexChartOptions({
  colors: ["#2499EF"],
  plotOptions: {
    bar: {
      borderRadius: 5,
      columnWidth: "15%",
      borderRadiusApplication: "end"
    }
  },
  xaxis: {
    crosshairs: { show: false },
    labels: { style: { colors: "#738499", fontSize: "12px", fontWeight: 500 } },
    categories: ["AF", "NA", "SA", "EU", "OC", "AS"]
  },
  yaxis: {
    min: 0,
    stepSize: 2500,
    tickAmount: 4,
    labels: {
      formatter: (value) => (value > 0 ? value / 1000 + "K" : value.toString()),
      style: { fontWeight: 600, colors: "#738499", fontSize: "11px" }
    }
  }
});

const series = ref([{ name: "users", data: [2556, 6555, 3666, 5833, 7477, 8544] }]);
</script>

<template>
  <Card class="px-5 py-6 col-span-full">
    <CardTitle class="mb-4">
      <h4 class="mb-1 text-sm font-semibold">Users by Continent</h4>
      <p class="text-xs font-medium text-muted">Top 7 Countries</p>
    </CardTitle>

    <div class="grid items-center grid-cols-12 gap-10">
      <div class="col-span-full lg:col-span-6">
        <div v-for="continent in usersByContinent" class="pe-20 border-e-border lg:border-e">
          <div class="flex items-center justify-between space-y-5">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full bg-primary"></div>
              <p class="text-sm font-medium">{{ continent.country }}</p>
            </div>

            <p class="text-sm font-medium">{{ continent.visitor }}</p>
          </div>
        </div>
      </div>

      <div class="col-span-full lg:col-span-6">
        <VueApexCharts type="bar" height="260" :options="chartOptions" :series="series" />
      </div>
    </div>
  </Card>
</template>
