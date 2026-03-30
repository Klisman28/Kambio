import { RouteRecordRaw } from "vue-router";

export const userRoutes: RouteRecordRaw[] = [
  {
    name: "Users",
    path: "/users",
    component: () => import("@/pages/users/Users.vue"),
    meta: { title: "Users" }
  },
  {
    name: "User",
    path: "/users/:id",
    component: () => import("@/pages/users/UserEdit.vue"),
    meta: { title: "User" }
  },
  {
    name: "NewUser",
    path: "/users/create",
    component: () => import("@/pages/users/UserCreate.vue"),
    meta: { title: "New User" }
  },
  {
    name: "UserProfile",
    path: "/users/profile",
    component: () => import("@/pages/users/UserProfile.vue"),
    meta: { title: "User Profile" }
  }
];
