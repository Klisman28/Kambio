import { createRouter, createWebHistory } from "vue-router";
import NProgress from "nprogress";
// AUTH COMPOSABLE
import { useAuth } from "@/theme/auth/useAuth";
// ROUTE GROUP FILES
import { userRoutes } from "./userRoutes";
import { orderRoutes } from "./orderRoutes";
import { productRoutes } from "./productRoutes";
import { invoiceRoutes } from "./invoiceRoutes";
import { sessionRoutes } from "./sessionRoutes";
import { supportRoutes } from "./supportRoutes";
import { settingsRoutes } from "./settingsRoutes";
import { dashboardRoutes } from "./dashboardRoutes";

// ==============================================================
declare module "vue-router" {
  interface RouteMeta {
    title?: string;
    requireAuth?: boolean;
  }
}
// ==============================================================

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import("@/theme/pages/home/index.vue"),
      meta: { requireAuth: false }
    },
    {
      path: "/dashboard",
      name: "Dashboards",
      redirect: "/learning-management",
      component: () => import("@/theme/layout/DefaultLayout.vue"),
      children: [
        ...dashboardRoutes,
        ...userRoutes,
        ...productRoutes,
        ...orderRoutes,
        ...invoiceRoutes,
        ...settingsRoutes,
        ...supportRoutes
      ],
      meta: { requireAuth: true }
    },

    {
      path: "/sessions",
      name: "Sessions",
      redirect: "/login",
      children: [...sessionRoutes],
      meta: { requireAuth: false }
    }
  ]
});

NProgress.configure({ showSpinner: false });

const DEFAULT_TITLE = "Uko - Admin & Client Dashboard Template";
const setDocumentTitle = (title?: string) => {
  document.title = title ? `${title} - ${DEFAULT_TITLE}` : DEFAULT_TITLE;
};

router.beforeEach(async (to, _from, next) => {
  if (to.name) NProgress.start();

  setDocumentTitle(to.meta.title);

  // WAIT FOR THE AUTH STATE TO BE READY
  const { waitForAuth, state } = useAuth();
  await waitForAuth();

  // CHECK IF THE USER IS AUTHENTICATED
  const requireAuth = to.matched.some((route) => route.meta.requireAuth);
  const isAuthenticated = !!state.user;

  // REDIRECT TO LOGIN IF NOT AUTHENTICATED
  if (requireAuth && !isAuthenticated) {
    return next({
      name: "Login",
      query: { redirect: to.fullPath }
    });
  }

  // REDIRECT TO DASHBOARD IF AUTHENTICATED
  if (!requireAuth && isAuthenticated) {
    return next({
      name: "Dashboards",
      replace: true
    });
  }

  next();
});

// COMPLETE THE ANIMATION OF THE ROUTE PROGRESS BAR.
router.afterEach(() => {
  NProgress.done();
});

export default router;
