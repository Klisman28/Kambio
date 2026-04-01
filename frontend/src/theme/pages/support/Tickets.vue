<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPONENT
import Icon from "@/theme/components/Icon.vue";
import AccordionWidget from "@/theme/sections/support/AccordionWidget.vue";
// DATA LIST
import { tickets } from "@/theme/data/support/tickets";
import { socialLinks } from "@/theme/data/support/social-links";

// STATE
const defaultValue = "item-1";
</script>

<template>
  <div class="grid grid-cols-12 gap-7 my-7">
    <Card class="p-6 col-span-full 2xl:col-span-9 xl:col-span-8">
      <CardTitle class="mb-6">All Tickets</CardTitle>
      <AccordionWidget :list="tickets" :default-value="defaultValue" />
    </Card>

    <Card class="self-start p-6 col-span-full 2xl:col-span-3 xl:col-span-4">
      <CardTitle class="mb-6">Follow Us</CardTitle>

      <div class="space-y-6">
        <div v-for="item in socialLinks" :key="item.id" class="flex items-center gap-3">
          <div class="flex items-center justify-center w-8 h-8 rounded-md bg-primary/10">
            <Icon :size="18" :strokeWidth="1.5" :name="item.icon" class="text-primary" />
          </div>

          <div>
            <h5 class="text-sm font-semibold">{{ item.name }}</h5>
            <p class="text-xs text-muted">
              {{ item.message }}
              <a :href="item.actionUrl" class="text-primary">
                {{ item.action }}
              </a>
            </p>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>
