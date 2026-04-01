import { RouteRecordRaw } from "vue-router";

export const settingsRoutes: RouteRecordRaw[] = [
  {
    path: "/settings",
    name: "Settings",
    component: () => import("@/theme/sections/settings/layout"),
    children: [
      {
        path: "",
        name: "ProfileInfo",
        component: () => import("@/theme/pages/settings/ProfileInfo.vue"),
        meta: { title: "Profile Settings" }
      },
      {
        path: "security",
        name: "Security",
        component: () => import("@/theme/pages/settings/Security.vue"),
        meta: { title: "Security Settings" }
      },
      {
        path: "plan-billing",
        name: "PlanBilling",
        component: () => import("@/theme/pages/settings/PlanBilling.vue"),
        meta: { title: "Plan & Billing" }
      },
      {
        path: "two-factor-authentication",
        name: "TwoFactorAuthentication",
        component: () => import("@/theme/pages/settings/TwoFactorAuth.vue"),
        meta: { title: "Two Factor Authentication" }
      },
      {
        path: "notification",
        name: "Notification",
        component: () => import("@/theme/pages/settings/Notification.vue"),
        meta: { title: "Notification" }
      },
      {
        path: "social-media-links",
        name: "SocialMediaLinks",
        component: () => import("@/theme/pages/settings/SocialMediaLinks.vue"),
        meta: { title: "Social Media Links" }
      },

      {
        path: "account-deactivation",
        name: "AccountDeactivation",
        component: () => import("@/theme/pages/settings/AccountDeactivation.vue"),
        meta: { title: "Account Deactivation" }
      }
    ]
  }
];
