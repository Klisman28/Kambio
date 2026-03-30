<script setup lang="ts">
import { useWindowScroll, useDark, useToggle, useTextDirection } from "@vueuse/core";
// CUSTOM STORE
import { useSidebar } from "@/stores/sidebar";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
import SearchPopover from "./popovers/SearchPopover.vue";
import ProfilePopover from "./popovers/ProfilePopover.vue";
import NotificationPopover from "./popovers/NotificationPopover.vue";

const isDark = useDark();
const dir = useTextDirection();
const toggleDark = useToggle(isDark);
const { y } = useWindowScroll({ behavior: "smooth" });

const sidebarStore = useSidebar();

const changeDirection = () => {
  dir.value = dir.value === "rtl" ? "ltr" : "rtl";
};

const handleFullScreen = () => {
  if (document.fullscreenElement) {
    document.exitFullscreen();
  } else {
    document.documentElement.requestFullscreen();
  }
};
</script>

<template>
  <header
    class="sticky top-0 py-5 w-full transition-all z-12"
    :class="{ 'backdrop-blur-xs shadow-xs': y > 0 }">
    <div
      class="flex justify-between items-center px-4 mx-auto max-w-(--breakpoint-2xl) sm:px-7 2xl:px-20">
      <div class="flex gap-2 items-center">
        <button class="lg:hidden" @click="sidebarStore.handleSidebarToggle()">
          <Icon name="Menu" class="text-primary" :strokeWidth="1.5" />
        </button>

        <SearchPopover />
      </div>

      <div class="flex items-center gap-[16px]">
        <button @click="handleFullScreen()">
          <Icon :size="20" :strokeWidth="1.5" name="Expand" class="text-muted" />
        </button>

        <button @click="changeDirection()">
          <Icon
            :size="20"
            :strokeWidth="1.5"
            :name="dir === 'rtl' ? 'AlignStartVertical' : 'AlignEndVertical'"
            class="text-muted" />
        </button>

        <button @click="toggleDark()">
          <Icon :size="20" :strokeWidth="1.5" name="Sun" v-if="isDark" class="text-warning" />
          <Icon :size="20" :strokeWidth="1.5" name="MoonStar" v-else class="text-muted" />
        </button>

        <NotificationPopover />

        <ProfilePopover />
      </div>
    </div>
  </header>
</template>
