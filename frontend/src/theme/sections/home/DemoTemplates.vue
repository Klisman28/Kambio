<script setup lang="ts">
import { Badge } from "@/theme/components/ui/badge";
import TemplateCard from "./TemplateCard.vue";
// DATA LIST
import { demos, managements, settings } from "@/theme/sections/home/data/demoList";
</script>

<template>
  <div class="py-24 bg-card">
    <div class="container px-4 mx-auto space-y-14">
      <div class="text-center">
        <h3 class="pt-6 text-xl leading-loose text-balance text-muted">
          Production Ready & Developer Friendly <br />
          <span class="text-2xl font-bold lg:text-4xl text-primary">Vue 3 Admin Template</span>
        </h3>
      </div>

      <div class="space-y-8 text-center">
        <Badge class="px-4 py-1 text-sm">Dashboard</Badge>

        <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <TemplateCard
            v-for="(item, index) in demos"
            :key="index"
            :image="item.image"
            :title="item.title"
            :route="item.route"
            :description="item.description" />
        </div>
      </div>

      <div class="space-y-8 text-center">
        <Badge class="px-4 py-1 text-sm">Management</Badge>

        <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <TemplateCard
            v-for="(item, index) in managements"
            :key="index"
            :image="item.image"
            :title="item.title"
            :route="item.route"
            :description="item.description" />
        </div>
      </div>

      <div class="space-y-8 text-center">
        <Badge class="px-4 py-1 text-sm">Settings</Badge>

        <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <TemplateCard
            v-for="(item, index) in settings"
            :key="index"
            :image="item.image"
            :title="item.title"
            :route="item.route"
            :description="item.description" />
        </div>
      </div>
    </div>
  </div>
</template>
