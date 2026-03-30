<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectItem,
  SelectGroup,
  SelectValue,
  SelectContent,
  SelectTrigger
} from "@/components/ui/select";
// CUSTOM COMPOSABLE
import { useApexChartOptions } from "@/hooks/useApexChartOptions";

const DATA = [
  [{ name: "sat", data: [31, 40, 28, 51, 40, 60, 50, 85] }],
  [{ name: "sun", data: [34, 40, 24, 51, 46, 60, 50, 85] }],
  [{ name: "mon", data: [31, 45, 28, 51, 42, 60, 60, 95] }]
];

// ==============================================================
interface Series {
  name: string;
  data: number[];
}
// ==============================================================

const selected = ref("0");
const series = ref<Series[]>(DATA[+selected.value]);

const handleChangeDay = (value: string) => {
  selected.value = value;
  series.value = DATA[+value];
};

const chartOptions = useApexChartOptions({
  grid: { show: true },
  chart: { type: "area" },
  stroke: { curve: "smooth" },
  colors: ["#2499EF", "#7EC9FF", "#E5F3FD"],
  xaxis: {
    offsetY: 10,
    labels: { style: { cssClass: "font-medium", colors: "#738499" } },
    categories: ["12 AM", "3 AM", "6 AM", "9 AM", "12 PM", "3 PM", "6 PM", "9 PM"],
    crosshairs: { stroke: { color: "#738499" } }
  },
  yaxis: {
    show: true,
    min: 0,
    max: 100,
    tickAmount: 4,
    labels: {
      offsetX: -12,
      formatter: (value: number) => value + "%",
      style: { cssClass: "font-medium", colors: "#738499" }
    }
  },

  responsive: [
    { breakpoint: 1440, options: { chart: { height: 260 } } },
    { breakpoint: 1300, options: { chart: { height: 240 } } },
    { breakpoint: 1250, options: { chart: { height: 200 } } },
    { breakpoint: 1050, options: { chart: { height: 150 } } },
    { breakpoint: 1020, options: { chart: { height: 300 } } },
    { breakpoint: 576, options: { chart: { height: 200 }, xaxis: { labels: { show: false } } } }
  ]
});
</script>

<template>
  <Card class="px-5 py-6 col-span-full 2xl:col-span-8 xl:col-span-7 lg:col-span-7">
    <div class="flex items-center justify-between mb-4">
      <CardTitle>Application Recieved Time</CardTitle>

      <Select v-model="selected" v-on:update:model-value="handleChangeDay($event)">
        <SelectTrigger
          class="text-[13px] font-semibold w-20 h-8 border-none rounded-lg bg-slate-100/40 dark:bg-slate-700/40">
          <SelectValue placeholder="Select a day" />
        </SelectTrigger>

        <SelectContent>
          <SelectGroup>
            <SelectItem value="0" class="text-[13px] font-medium">Sat</SelectItem>
            <SelectItem value="1" class="text-[13px] font-medium">Sun</SelectItem>
            <SelectItem value="2" class="text-[13px] font-medium">Mon</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
    </div>

    <VueApexCharts type="area" height="300" :options="chartOptions" :series="series" />
  </Card>
</template>
