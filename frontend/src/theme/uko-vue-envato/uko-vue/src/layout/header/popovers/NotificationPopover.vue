<script setup lang="ts">
import { Ban, BellRing } from "lucide-vue-next";
// SHADCDN COMPONENTS
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
// DATA LIST
import { notifications } from "@/data/notifications";
</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <button>
        <BellRing :strokeWidth="1.5" :size="20" class="text-primary" />
      </button>
    </PopoverTrigger>

    <PopoverContent class="w-[350px] p-0 py-3 mt-2">
      <div v-if="notifications.length === 0" class="flex flex-col gap-2 items-center px-3 py-10">
        <Ban class="text-slate-400" :size="30" />
        <p class="text-sm">No new notifications</p>
      </div>

      <div v-else>
        <p class="px-4 pt-1 pb-4 text-base font-medium border-b border-border">Notification</p>

        <div
          :key="item.id"
          v-for="item in notifications"
          class="px-3 border-b cursor-pointer border-b-border hover:bg-hover"
          :class="{ 'bg-hover': !item.isRead }">
          <div class="flex gap-4 items-center py-4 group">
            <span
              class="w-2 h-2 rounded-full transition-all group-hover:bg-primary"
              :class="{ 'bg-slate-400': item.isRead, 'bg-primary': !item.isRead }">
            </span>

            <Avatar>
              <AvatarImage :src="item.image" alt="User" />
              <AvatarFallback>CN</AvatarFallback>
            </Avatar>

            <div class="overflow-hidden grow">
              <p class="text-sm font-semibold text-nowrap">
                {{ item.userName }}
              </p>

              <p class="pt-1 text-xs truncate text-muted">
                {{ item.message }}
              </p>
            </div>
          </div>
        </div>

        <RouterLink
          to="/"
          class="block px-3 pt-3 pb-1 text-sm font-medium text-center transition-all text-primary hover:underline">
          View All Notification
        </RouterLink>
      </div>
    </PopoverContent>
  </Popover>
</template>
