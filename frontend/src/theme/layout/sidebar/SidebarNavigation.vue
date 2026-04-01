<script setup lang="ts">
import Scrollbar from "simplebar-vue";
// CUSTOM COMPONENT
import NavItem from "./NavItem.vue";
// MENU LIST
import { navigation } from "@/theme/data/navigation";
</script>

<template>
  <div class="px-4 py-5 mb-2">
    <RouterLink to="/">
      <img src="/logos/uko.png" class="w-7 cursor-pointer" alt="Uko Admin & Client Dashboard" />
    </RouterLink>
  </div>

  <Scrollbar class="h-[calc(100vh-75px)]">
    <nav class="pb-4 space-y-6">
      <div class="space-y-3" v-for="navGroup in navigation" :key="navGroup.id">
        <h4 class="px-5 text-[12px] font-semibold text-primary uppercase">
          {{ navGroup.name }}
        </h4>

        <ul>
          <NavItem v-for="(menuItem, index) in navGroup.menu" :item="menuItem" :key="index" />
        </ul>
      </div>
    </nav>
  </Scrollbar>
</template>
