<script setup lang="ts">
import Header from "./header/Header.vue";
import MobileSidebar from "./MobileSidebar.vue";
import SidebarNavigation from "./sidebar/SidebarNavigation.vue";
</script>

<template>
  <!-- SIDEBAR NAVIGATION SECTION FOR DESKTOP DEVICE -->
  <aside
    class="bg-white h-screen fixed left-0 w-[260px] 2xl:w-[280px] top-0 z-1111 hidden lg:block dark:bg-background rtl:right-0 rtl:left-auto">
    <SidebarNavigation />
  </aside>

  <main class="h-full lg:ml-[260px] 2xl:ml-[280px] rtl:mr-[260px] 2xl:rtl:mr-[280px] rtl:ml-auto">
    <!-- HEADER SECTION -->
    <Header></Header>

    <!-- NAVIGATION DRAWER FOR SMALL DEVICE -->
    <MobileSidebar />

    <!-- PAGE / ROUTE VIEW -->
    <div class="px-4 mx-auto max-w-(--breakpoint-2xl) sm:px-7 2xl:px-20">
      <RouterView />
    </div>
  </main>
</template>
