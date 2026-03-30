<script setup lang="ts">
import BulletListItem from "./BulletListItem.vue";

defineProps<{ list: string[] }>();
</script>

<template>
  <ul class="text-sm space-y-4 col-span-full md:col-span-6 lg:col-span-4">
    <BulletListItem v-for="(item, index) in list" :key="index" :item="item" />
  </ul>
</template>
