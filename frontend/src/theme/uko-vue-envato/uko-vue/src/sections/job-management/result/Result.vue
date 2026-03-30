<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/components/ui/card";
// CUSTOM COMPONENT
import ListItem from "./ListItem.vue";
// LIST DATA
import { result } from "@/data/dashboards/job-management";
</script>

<template>
  <Card class="px-5 py-6 col-span-full lg:col-span-6 self-start">
    <CardTitle class="mb-7">Result</CardTitle>
    <div class="space-y-7">
      <ListItem v-for="data in result" :key="data.id" :title="data.title" :value="data.value" />
    </div>
  </Card>
</template>
