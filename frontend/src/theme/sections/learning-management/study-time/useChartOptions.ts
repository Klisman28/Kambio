import { ref } from "vue";
import { useApexChartOptions } from "@/theme/hooks/useApexChartOptions";

export const useChartOptions = () => {
  const series = ref([
    { name: "React", data: [20, 30, 40, 50, 40, 30, 20] },
    { name: "Angular", data: [30, 30, 30, 30, 30, 30, 30] },
    { name: "Javascript", data: [20, 20, 20, 20, 20, 20, 20] }
  ]);

  const chartOptions = useApexChartOptions({
    yaxis: { show: false },
    chart: { type: "bar", stacked: true },
    colors: ["#2499EF", "#7EC9FF", "#E5F3FD"],
    plotOptions: {
      bar: {
        horizontal: false,
        borderRadius: 7,
        columnWidth: "25%"
      }
    },
    legend: {
      show: true,
      fontWeight: 500,
      fontSize: "12px",
      position: "bottom",
      horizontalAlign: "center",
      onItemClick: { toggleDataSeries: false },
      onItemHover: { highlightDataSeries: false },
      itemMargin: { horizontal: 10, vertical: 10 },
      markers: { offsetX: -5, strokeWidth: 0, size: 6, shape: "circle" }
    },
    xaxis: {
      offsetY: -5,
      axisTicks: { show: false },
      axisBorder: { show: false },
      crosshairs: { show: false },
      categories: ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"],
      labels: { style: { fontSize: "10px", fontWeight: 500 } }
    },
    responsive: [
      {
        breakpoint: 1600,
        options: {
          plotOptions: { bar: { borderRadius: 5 } }
        }
      },
      {
        breakpoint: 1439,
        options: {
          plotOptions: { bar: { borderRadius: 12 } }
        }
      },
      {
        breakpoint: 1280,
        options: {
          plotOptions: { bar: { borderRadius: 12 } }
        }
      },
      {
        breakpoint: 769,
        options: {
          chart: { height: 400 },
          plotOptions: { bar: { borderRadius: 10 } }
        }
      },
      {
        breakpoint: 575,
        options: {
          chart: { height: 300 },
          plotOptions: { bar: { borderRadius: 6 } }
        }
      },
      {
        breakpoint: 376,
        options: {
          chart: { height: 250 },
          plotOptions: { bar: { borderRadius: 5 } }
        }
      }
    ]
  });

  return { chartOptions, series };
};
