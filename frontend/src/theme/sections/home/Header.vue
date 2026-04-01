<script setup lang="ts">
import { useWindowScroll, useDark, useToggle } from "@vueuse/core";
import { RouterLink } from "vue-router";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
// CUSTOM UTILS METHOD
import { cn } from "@/theme/lib/utils";

const isDark = useDark();
const toggleDark = useToggle(isDark);
const { y } = useWindowScroll({ behavior: "smooth" });
</script>

<template>
  <header
    :class="
      cn({
        'sticky top-0 z-12 w-full py-5 transition-all': true,
        'backdrop-blur-lg bg-transparent shadow-xs': y > 0
      })
    ">
    <div class="container px-4 mx-auto">
      <div class="flex justify-between items-center">
        <RouterLink to="/">
          <img src="/logos/uko.png" alt="Uko Admin & Client Dashboard" class="w-7 shrink-0" />
        </RouterLink>

        <button @click="toggleDark()">
          <Icon :size="22" name="Sun" v-if="isDark" class="text-warning" />
          <Icon :size="22" name="Moon" v-else class="text-muted" />
        </button>
      </div>
    </div>
  </header>
</template>
