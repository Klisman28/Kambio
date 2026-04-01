import { RouteRecordRaw } from "vue-router";

export const supportRoutes: RouteRecordRaw[] = [
  {
    name: "Support",
    path: "/support",
    component: () => import("@/theme/sections/support/layout"),
    children: [
      {
        path: "",
        name: "SupportOverview",
        component: () => import("@/theme/pages/support/Overview.vue"),
        meta: { title: "Support Overview" }
      },
      {
        path: "tickets",
        name: "Tickets",
        component: () => import("@/theme/pages/support/Tickets.vue"),
        meta: { title: "Tickets" }
      },
      {
        path: "faqs",
        name: "FAQs",
        component: () => import("@/theme/pages/support//Faqs.vue"),
        meta: { title: "FAQs" }
      },
      {
        path: "contact",
        name: "Contact",
        component: () => import("@/theme/pages/support/Contact.vue"),
        meta: { title: "Contact" }
      },
      {
        path: "create-ticket",
        name: "CreateTicket",
        component: () => import("@/theme/pages/support/CreateTicket.vue"),
        meta: { title: "Create Ticket" }
      }
    ]
  }
];
