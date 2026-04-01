import { RouteRecordRaw } from "vue-router";

export const userRoutes: RouteRecordRaw[] = [
  {
    name: "Users",
    path: "/users",
    component: () => import("@/theme/pages/users/Users.vue"),
    meta: { title: "Users" }
  },
  {
    name: "User",
    path: "/users/:id",
    component: () => import("@/theme/pages/users/UserEdit.vue"),
    meta: { title: "User" }
  },
  {
    name: "NewUser",
    path: "/users/create",
    component: () => import("@/theme/pages/users/UserCreate.vue"),
    meta: { title: "New User" }
  },
  {
    name: "UserProfile",
    path: "/users/profile",
    component: () => import("@/theme/pages/users/UserProfile.vue"),
    meta: { title: "User Profile" }
  }
];
