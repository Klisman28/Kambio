<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// CUSTOM COMPOSABLE
import { useApexChartOptions } from "@/hooks/useApexChartOptions";
// SHADCN COMPONENTS
import {
  Select,
  SelectItem,
  SelectGroup,
  SelectValue,
  SelectContent,
  SelectTrigger
} from "@/components/ui/select";
import { Card } from "@/components/ui/card";

const selected = ref("0");
const series = ref([
  { name: "Leads", data: [50, 170, 120, 80, 90, 170, 90] },
  { name: "Customers", data: [150, 52, 100, 152, 94, 152, 100] }
]);

const chartOptions = useApexChartOptions({
  grid: { show: true },
  colors: ["#FFC675", "#2499EF"],
  stroke: { curve: "smooth", width: 3 },
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
      style: { colors: "#738499", fontSize: "11px", fontWeight: 500 }
    },

    axisBorder: { show: false },
    axisTicks: { show: false },
    tooltip: { enabled: false }
  },
  legend: {
    show: true,
    offsetY: 6,
    fontWeight: 600,
    fontSize: "12px",
    position: "top",
    horizontalAlign: "center",
    itemMargin: { horizontal: 15, vertical: 0 },
    markers: { offsetX: -5, size: 6, shape: "circle" }
  },
  yaxis: {
    min: 0,
    stepSize: 50,
    tickAmount: 4,
    labels: {
      offsetX: -5,
      style: {
        fontWeight: 600,
        colors: "#738499",
        fontSize: "11px"
      }
    }
  },
  responsive: [
    { breakpoint: 1450, options: { chart: { height: 280 } } },
    { breakpoint: 1280, options: { chart: { height: 230 } } },
    { breakpoint: 1080, options: { chart: { height: 180 } } },
    { breakpoint: 780, options: { chart: { height: 300 } } },
    { breakpoint: 575, options: { chart: { height: 250 } } }
  ]
});
</script>

<template>
  <Card class="pt-6 pb-2 col-span-full lg:col-span-8 self-start">
    <div class="flex items-center justify-between px-5 mb-4">
      <p class="text-sm font-semibold">Leads vs Customers</p>
      <Select v-model:model-value="selected">
        <SelectTrigger
          class="text-[13px] font-semibold w-20 h-8 border-none rounded-lg bg-slate-100/40 dark:bg-slate-700/40">
          <SelectValue placeholder="Select a day" />
        </SelectTrigger>

        <SelectContent>
          <SelectGroup>
            <SelectItem value="0" class="text-[13px] font-medium">Week</SelectItem>
            <SelectItem value="1" class="text-[13px] font-medium">Month</SelectItem>
            <SelectItem value="2" class="text-[13px] font-medium">Year</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
    </div>

    <div class="pl-2 pr-4">
      <VueApexCharts type="area" height="330" :options="chartOptions" :series="series" />
    </div>
  </Card>
</template>
