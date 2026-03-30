import { RouteRecordRaw } from "vue-router";

export const supportRoutes: RouteRecordRaw[] = [
  {
    name: "Support",
    path: "/support",
    component: () => import("@/sections/support/layout"),
    children: [
      {
        path: "",
        name: "SupportOverview",
        component: () => import("@/pages/support/Overview.vue"),
        meta: { title: "Support Overview" }
      },
      {
        path: "tickets",
        name: "Tickets",
        component: () => import("@/pages/support/Tickets.vue"),
        meta: { title: "Tickets" }
      },
      {
        path: "faqs",
        name: "FAQs",
        component: () => import("@/pages/support//Faqs.vue"),
        meta: { title: "FAQs" }
      },
      {
        path: "contact",
        name: "Contact",
        component: () => import("@/pages/support/Contact.vue"),
        meta: { title: "Contact" }
      },
      {
        path: "create-ticket",
        name: "CreateTicket",
        component: () => import("@/pages/support/CreateTicket.vue"),
        meta: { title: "Create Ticket" }
      }
    ]
  }
];
