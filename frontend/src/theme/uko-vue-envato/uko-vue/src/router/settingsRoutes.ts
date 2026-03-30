import { RouteRecordRaw } from "vue-router";

export const settingsRoutes: RouteRecordRaw[] = [
  {
    path: "/settings",
    name: "Settings",
    component: () => import("@/sections/settings/layout"),
    children: [
      {
        path: "",
        name: "ProfileInfo",
        component: () => import("@/pages/settings/ProfileInfo.vue"),
        meta: { title: "Profile Settings" }
      },
      {
        path: "security",
        name: "Security",
        component: () => import("@/pages/settings/Security.vue"),
        meta: { title: "Security Settings" }
      },
      {
        path: "plan-billing",
        name: "PlanBilling",
        component: () => import("@/pages/settings/PlanBilling.vue"),
        meta: { title: "Plan & Billing" }
      },
      {
        path: "two-factor-authentication",
        name: "TwoFactorAuthentication",
        component: () => import("@/pages/settings/TwoFactorAuth.vue"),
        meta: { title: "Two Factor Authentication" }
      },
      {
        path: "notification",
        name: "Notification",
        component: () => import("@/pages/settings/Notification.vue"),
        meta: { title: "Notification" }
      },
      {
        path: "social-media-links",
        name: "SocialMediaLinks",
        component: () => import("@/pages/settings/SocialMediaLinks.vue"),
        meta: { title: "Social Media Links" }
      },

      {
        path: "account-deactivation",
        name: "AccountDeactivation",
        component: () => import("@/pages/settings/AccountDeactivation.vue"),
        meta: { title: "Account Deactivation" }
      }
    ]
  }
];
