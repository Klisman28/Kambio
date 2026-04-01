<script setup lang="ts">
import { useRoute } from "vue-router";
import { RouterLink } from "vue-router";
// SHADCN COMPONENTS
import { Input } from "@/theme/components/ui/input";
import { Button } from "@/theme/components/ui/button";
import { Card, CardContent } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
// DATA LIST
const supportNavigation = [
  { label: "Overview", route: "/support" },
  { label: "Tickets", route: "/support/tickets" },
  { label: "FAQs", route: "/support/faqs" },
  { label: "Contact", route: "/support/contact" }
];

const route = useRoute();
</script>

<template>
  <Card class="px-5 py-6 mb-2 col-span-full">
    <CardContent class="space-y-6 xl:space-y-8">
      <div class="flex items-center gap-20 sm:px-10 xl:px-20 xl:gap-32">
        <img
          src="/images/illustration/support-1.svg"
          alt="Illustration"
          class="hidden w-72 xl:block" />

        <div class="flex flex-col items-center w-full py-5 space-y-5 xl:items-start">
          <h5 class="text-2xl font-semibold">How Can We Help You?</h5>

          <div class="relative mb-3">
            <Input
              type="text"
              name="ask-your-questions"
              placeholder="Ask you questions"
              class="w-full ps-10 max-w-96" />

            <Icon
              name="Search"
              :size="18"
              :strokeWidth="2"
              class="absolute inset-y-0 my-auto text-muted start-3" />
          </div>
        </div>
      </div>

      <div
        class="flex flex-col items-center justify-center gap-4 px-4 py-3 rounded-lg bg-slate-100/50 dark:bg-slate-700/10 lg:flex-row lg:justify-between">
        <div class="flex flex-wrap justify-center gap-1 md:justify-start">
          <RouterLink
            v-for="nav in supportNavigation"
            :to="nav.route"
            class="inline-flex items-center px-4 py-2 text-xs font-medium tracking-wider uppercase rounded-lg xl:px-6 text-muted"
            :class="{ 'bg-primary/10 text-primary': nav.route === route.path }">
            {{ nav.label }}
          </RouterLink>
        </div>

        <Button :as="RouterLink" to="/support/create-ticket" class="w-full lg:w-auto">
          Create Ticket
        </Button>
      </div>
    </CardContent>
  </Card>
</template>
