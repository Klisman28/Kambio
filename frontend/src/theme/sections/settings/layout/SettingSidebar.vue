<script setup lang="ts">
import { useRoute } from "vue-router";
// SHADCN COMPONENTS
import { Card, CardContent } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
// DATA LIST
const navigation = [
  { icon: "AppWindow", label: "Profile Info", route: "/settings" },
  { icon: "Fingerprint", label: "Security", route: "/settings/security" },
  { icon: "CreditCard", label: "Plan & Billing", route: "/settings/plan-billing" },
  {
    icon: "ShieldCheck",
    label: "Two Factor Authentication",
    route: "/settings/two-factor-authentication"
  },
  { icon: "Bell", label: "Notification", route: "/settings/notification" },
  { icon: "Podcast", label: "Social Media Links", route: "/settings/social-media-links" },
  { icon: "Trash", label: "Account Deactivation", route: "/settings/account-deactivation" }
];

const route = useRoute();
</script>

<template>
  <div class="sticky top-0">
    <Card class="py-2">
      <CardContent>
        <RouterLink
          v-for="nav in navigation"
          :to="nav.route"
          :key="nav.route"
          class="text-sm flex items-center gap-3 py-3.5 px-5 xl:px-8 cursor-pointer hover:bg-primary/10 hover:text-primary duration-300"
          :class="{ 'bg-primary/10 text-primary': route.path == nav.route }">
          <Icon :name="nav.icon" :size="20" /> {{ nav.label }}
        </RouterLink>
      </CardContent>
    </Card>
  </div>
</template>
