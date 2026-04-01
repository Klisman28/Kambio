<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import BulletList from "@/theme/sections/support/BulletList.vue";
import AccordionWidget from "@/theme/sections/support/AccordionWidget.vue";
// DATA LIST
import { tickets } from "@/theme/data/support/tickets";
import { features } from "@/theme/data/support/features";

// STATE
const defaultValue = "item-1";
</script>

<template>
  <div class="grid grid-cols-12 gap-7 my-7">
    <Card class="p-6 col-span-full xl:col-span-6">
      <CardTitle class="mb-6">Support Tickets</CardTitle>
      <AccordionWidget :list="tickets" :defaultValue="defaultValue" />
    </Card>

    <Card class="p-6 col-span-full xl:col-span-6">
      <CardTitle class="mb-6">FAQs</CardTitle>
      <AccordionWidget :list="tickets" :defaultValue="defaultValue" />
    </Card>
  </div>

  <Card class="relative p-6">
    <CardTitle class="mb-6">Documentations</CardTitle>

    <CardContent class="grid grid-cols-12 gap-4">
      <BulletList :list="features.slice(0, 6)" />
      <BulletList :list="features.slice(6, 12)" />
      <BulletList :list="features.slice(12)" />

      <img
        src="/images/illustration/support-2.svg"
        alt="Illustration"
        class="absolute bottom-0 right-0 hidden w-60 xl:block rtl:left-0 rtl:right-auto" />
    </CardContent>
  </Card>
</template>
