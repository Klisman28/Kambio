<script setup lang="ts">
import { useRoute, RouterLink } from "vue-router";
// CUSTOM COMPONENT
import Icon from "@/theme/components/Icon.vue";
import NavAccordion from "./NavAccordion.vue";
// CUSTOM STORE
import { useSidebar } from "@/theme/stores/sidebar";
// TYPE
import { NavItem } from "./type";

defineProps<{ item: NavItem }>();

const route = useRoute();
const { handleCloseSidebar } = useSidebar();
</script>

<template>
  <li v-if="item.children">
    <NavAccordion :item="item" />
  </li>

  <li
    v-else
    @click="handleCloseSidebar()"
    class="transition-all duration-300 ease-in-out border-l-2 cursor-pointer text-muted group border-l-transparent hover:font-medium hover:border-l-primary hover:text-primary hover:bg-hover"
    :class="{ 'bg-hover border-l-primary! text-primary': route.path === item.route }">
    <RouterLink
      :to="item.route"
      class="flex p-4 text-[13px] font-medium truncate items-center gap-3">
      <Icon :size="20" :name="item.icon" :strokeWidth="1.5" />

      {{ item.label }}
    </RouterLink>
  </li>
</template>
