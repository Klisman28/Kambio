<script setup lang="ts">
// CUSTOM COMPONENTS
import FeatureCard from "./FeatureCard.vue";
// DATA LIST
import { features } from "@/theme/sections/home/data/featureList";
</script>

<template>
  <div class="py-24">
    <div class="container px-4 mx-auto space-y-14">
      <div class="text-center">
        <p class="text-base font-medium truncate text-muted">Almost covered everything</p>

        <h3 class="pt-3 text-2xl font-bold lg:text-3xl text-balance">
          Other Amazing Features & Flexibility Provided
        </h3>
      </div>

      <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <FeatureCard
          v-for="(item, index) in features"
          :key="index"
          :title="item.title"
          :description="item.description"
          :iconName="item.icon"
          :color="item.color" />
      </div>
    </div>
  </div>
</template>
