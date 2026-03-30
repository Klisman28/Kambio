import { RouteRecordRaw } from "vue-router";

export const invoiceRoutes: RouteRecordRaw[] = [
  {
    name: "Invoices",
    path: "/invoices",
    component: () => import("@/pages/invoices/Invoices.vue"),
    meta: { title: "Invoices" }
  },
  {
    name: "InvoiceEdit",
    path: "/invoices/:id",
    component: () => import("@/pages/invoices/InvoiceEdit.vue"),
    meta: { title: "Invoice Edit" }
  },
  {
    name: "InvoiceCreate",
    path: "/invoices/create",
    component: () => import("@/pages/invoices/InvoiceCreate.vue"),
    meta: { title: "Create Invoice" }
  },
  {
    name: "InvoiceDetails",
    path: "/invoices/:id/details",
    component: () => import("@/pages/invoices/InvoiceOverview.vue"),
    meta: { title: "Invoice Overview" }
  }
];
