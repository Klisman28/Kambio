import { RouteRecordRaw } from "vue-router";

export const orderRoutes: RouteRecordRaw[] = [
  {
    name: "Orders",
    path: "/orders",
    component: () => import("@/pages/orders/Orders.vue"),
    meta: { title: "Orders" }
  },

  {
    name: "OrderDetails",
    path: "/orders/:id",
    component: () => import("@/pages/orders/OrderOverview.vue"),
    meta: { title: "Order Details" }
  }
];
