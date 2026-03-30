<script setup lang="ts">
import {
  Menubar,
  MenubarItem,
  MenubarMenu,
  MenubarContent,
  MenubarTrigger
} from "@/components/ui/menubar";
import Icon from "@/components/Icon.vue";

defineProps<{ title: string; value: number; description: string }>();
</script>

<template>
  <div class="flex justify-between items-center py-2">
    <div class="flex items-center">
      <div class="flex items-center gap-3">
        <div class="grid place-items-center w-12 h-12 rounded-md bg-primary">
          <p class="text-2xl font-semibold text-white">{{ value }}</p>
        </div>

        <div>
          <p class="text-sm font-semibold">
            {{ title }}
          </p>

          <p class="text-[13px] text-muted mt-1">
            {{ description }}
          </p>
        </div>
      </div>
    </div>

    <Menubar class="justify-center p-0 bg-transparent">
      <MenubarMenu>
        <MenubarTrigger class="p-1 w-6 h-6 rounded-sm bg-slate-100 dark:bg-slate-800">
          <Icon name="Ellipsis" :size="18" />
        </MenubarTrigger>

        <MenubarContent align="end">
          <MenubarItem class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover">
            <Icon name="Eye" :size="18" class="text-muted" /> View
          </MenubarItem>

          <MenubarItem class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover">
            <Icon name="Trash" :size="18" class="text-muted" /> Delete
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>
    </Menubar>
  </div>
</template>
