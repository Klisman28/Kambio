import { useApexChartOptions } from "@/hooks/useApexChartOptions";

export const chartOptions = useApexChartOptions({
  colors: ["#2499EF"],
  legend: { show: false },
  tooltip: { enabled: false },
  stroke: { curve: "smooth", lineCap: "round" },
  plotOptions: {
    radialBar: {
      hollow: { size: "53%" },
      track: { strokeWidth: "100%", background: "#E5F3FD" },
      dataLabels: {
        name: { show: false },
        value: {
          offsetY: 5,
          fontSize: "14px",
          fontWeight: 600,
          color: "#2499EF",
          formatter: (value) => value + "%"
        }
      }
    }
  }
});
