<script setup lang="ts">
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { Avatar, AvatarFallback } from "@/theme/components/ui/avatar";
import { Popover, PopoverContent, PopoverTrigger } from "@/theme/components/ui/popover";
import Icon from "@/theme/components/Icon.vue";
import { useAuthStore } from "@/modules/auth/stores/authStore";

const router = useRouter();
const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

const initials = () => {
  const name = user.value?.full_name ?? "";
  return name.split(" ").map((w) => w[0]).slice(0, 2).join("").toUpperCase() || "K";
};

const handleLogout = () => {
  authStore.logout();
  router.replace({ name: "login" });
};
</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <div class="flex gap-2 items-center py-2 pr-2 pl-3 rounded-full cursor-pointer bg-hover">
        <p class="text-[13px] font-semibold text-nowrap">
          {{ user?.full_name ?? "Usuario" }}
        </p>
        <Avatar size="xs" class="border border-white">
          <AvatarFallback>{{ initials() }}</AvatarFallback>
        </Avatar>
      </div>
    </PopoverTrigger>

    <PopoverContent class="w-[180px] py-2 px-0 rounded-lg">
      <ul class="text-sm cursor-pointer">
        <li class="px-5 py-2 text-xs text-muted font-medium truncate">
          {{ user?.email ?? "" }}
        </li>
        <li class="py-1">
          <hr class="border-0 border-b border-b-gray-200 dark:border-b-gray-700" />
        </li>
        <li
          class="flex gap-2 items-center px-5 py-2 transition-all hover:bg-hover text-error"
          @click="handleLogout()">
          <Icon name="LogOut" :size="16" /> Cerrar sesión
        </li>
      </ul>
    </PopoverContent>
  </Popover>
</template>
