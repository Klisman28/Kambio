import { RouteRecordRaw } from "vue-router";

export const dashboardRoutes: RouteRecordRaw[] = [
  {
    name: "learningManagement",
    path: "/learning-management",
    component: () => import("@/pages/dashboard/LearningManagement.vue"),
    meta: { title: "Learning Dashboard" }
  },
  {
    name: "jobManagement",
    path: "/job-management",
    component: () => import("@/pages/dashboard/JobManagement.vue"),
    meta: { title: "Job Management" }
  },
  {
    name: "analytics",
    path: "/analytics",
    component: () => import("@/pages/dashboard/Analytics.vue"),
    meta: { title: "Analytics" }
  },
  {
    name: "sales",
    path: "/sales",
    component: () => import("@/pages/dashboard/Sales.vue"),
    meta: { title: "Sales" }
  },
  {
    name: "saas",
    path: "/saas",
    component: () => import("@/pages/dashboard/Saas.vue"),
    meta: { title: "Saas" }
  }
];
