<script setup lang="ts">
import { ref } from "vue";
import VueApexCharts from "vue3-apexcharts";
// SHADCN COMPONENTS
import {
  Select,
  SelectItem,
  SelectGroup,
  SelectValue,
  SelectContent,
  SelectTrigger
} from "@/components/ui/select";
import { Card, CardTitle } from "@/components/ui/card";
// CUSTOM COMPOSABLE
import { useApexChartOptions } from "@/hooks/useApexChartOptions";

const selected = ref("0");
const series = ref([
  {
    name: "Manager",
    data: [15000, 5000, 12000, 5500, 7500, 15000, 3000, 15000, 13000, 14000, 4000, 15000]
  }
]);

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
        chart: { height: 350 },
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
</script>

<template>
  <Card class="pt-6 col-span-full xl:col-span-6">
    <CardTitle class="flex items-start justify-between px-5">
      <p>Earnings Report</p>

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
    </CardTitle>

    <div class="pl-2 pr-4">
      <VueApexCharts type="bar" height="250" :options="chartOptions" :series="series" />
    </div>
  </Card>
</template>
