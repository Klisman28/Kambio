<script setup lang="ts">
import { VisuallyHidden } from "radix-vue";
// SHADCN COMPONENTS
import {
  Sheet,
  SheetTitle,
  SheetHeader,
  SheetContent,
  SheetDescription
} from "@/components/ui/sheet";
// CUSTOM COMPONENTS
import SidebarNavigation from "./sidebar/SidebarNavigation.vue";
// CUSTOM COMPOSABLE
import { useSidebar } from "@/stores/sidebar";

const sidebarStore = useSidebar();
</script>

<template>
  <Sheet :open="sidebarStore.isSidebarOpen" @update:open="sidebarStore.handleSidebarToggle()">
    <SheetContent side="left" class="p-0 outline-hidden border-r-0 w-[280px]">
      <VisuallyHidden>
        <SheetHeader>
          <SheetTitle>Uko</SheetTitle>
          <SheetDescription>Uko Admin & Client Dashboard Template</SheetDescription>
        </SheetHeader>
      </VisuallyHidden>

      <SidebarNavigation />
    </SheetContent>
  </Sheet>
</template>
