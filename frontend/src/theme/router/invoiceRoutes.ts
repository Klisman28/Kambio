import { RouteRecordRaw } from "vue-router";

export const invoiceRoutes: RouteRecordRaw[] = [
  {
    name: "Invoices",
    path: "/invoices",
    component: () => import("@/theme/pages/invoices/Invoices.vue"),
    meta: { title: "Invoices" }
  },
  {
    name: "InvoiceEdit",
    path: "/invoices/:id",
    component: () => import("@/theme/pages/invoices/InvoiceEdit.vue"),
    meta: { title: "Invoice Edit" }
  },
  {
    name: "InvoiceCreate",
    path: "/invoices/create",
    component: () => import("@/theme/pages/invoices/InvoiceCreate.vue"),
    meta: { title: "Create Invoice" }
  },
  {
    name: "InvoiceDetails",
    path: "/invoices/:id/details",
    component: () => import("@/theme/pages/invoices/InvoiceOverview.vue"),
    meta: { title: "Invoice Overview" }
  }
];
