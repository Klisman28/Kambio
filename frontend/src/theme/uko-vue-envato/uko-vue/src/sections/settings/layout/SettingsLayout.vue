<script setup lang="ts">
import SettingSidebar from "./SettingSidebar.vue";
</script>

<template>
  <div class="grid grid-cols-12 mt-2 mb-6 gap-7">
    <div class="col-span-full lg:col-span-4">
      <SettingSidebar />
    </div>

    <div class="col-span-full lg:col-span-8">
      <RouterView />
    </div>
  </div>
</template>
