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
const series = ref([75, 60, 30]);

const chartOptions = useApexChartOptions({
  stroke: { lineCap: "round" },
  labels: ["Sale", "Orders", "Return"],
  colors: ["#2499EF", "#FE8969", "#FF316F"],
  plotOptions: {
    radialBar: {
      hollow: { size: "28%" },
      track: { margin: 12, background: "#E5F3FD" },
      dataLabels: {
        name: { show: false },
        value: { fontSize: "18px", fontWeight: 700, offsetY: 8 }
      }
    }
  },
  legend: {
    show: true,
    offsetY: -12,
    fontWeight: 500,
    position: "bottom",
    horizontalAlign: "center",
    itemMargin: { horizontal: 12 },
    onItemClick: { toggleDataSeries: false },
    onItemHover: { highlightDataSeries: false },
    markers: { offsetX: -5, offsetY: 1, size: 6, shape: "circle" }
  }
});
</script>

<template>
  <Card class="px-5 pt-6 pb-5 col-span-full md:pb-0 xl:col-span-4">
    <div class="flex items-center justify-between">
      <p class="text-sm font-semibold">Analytics</p>

      <Select v-model:model-value="selected">
        <SelectTrigger
          class="text-[13px] font-semibold w-14 h-auto p-0 border-none rounded-lg bg-transparent outline-hidden focus:ring-0 focus:ring-offset-0">
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

    <VueApexCharts type="radialBar" height="320" :options="chartOptions" :series="series" />
  </Card>
</template>
