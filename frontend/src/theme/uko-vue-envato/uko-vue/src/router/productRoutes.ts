import { RouteRecordRaw } from "vue-router";

export const productRoutes: RouteRecordRaw[] = [
  {
    name: "Products",
    path: "/products",
    component: () => import("@/pages/products/Products.vue"),
    meta: { title: "Products" }
  },

  {
    name: "ProductEdit",
    path: "/products/:id",
    component: () => import("@/pages/products/ProductEdit.vue"),
    meta: { title: "Product Edit" }
  },
  {
    name: "ProductCreate",
    path: "/products/create",
    component: () => import("@/pages/products/ProductCreate.vue"),
    meta: { title: "New Product Create" }
  },
  {
    name: "ProductOverview",
    path: "/products/:id/overview",
    component: () => import("@/pages/products/ProductOverview.vue"),
    meta: { title: "Product Overview" }
  }
];
