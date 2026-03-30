import { RouteRecordRaw } from "vue-router";

export const sessionRoutes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/pages/sessions/Login.vue"),
    meta: { title: "Login" }
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/pages/sessions/Register.vue"),
    meta: { title: "Register" }
  },
  {
    path: "/forget-password",
    name: "ForgetPassword",
    component: () => import("@/pages/sessions/ForgetPassword.vue"),
    meta: { title: "Forget Password" }
  },
  {
    path: "/verification",
    name: "Verification",
    component: () => import("@/pages/sessions/Verification.vue"),
    meta: { title: "Verification" }
  }
];
