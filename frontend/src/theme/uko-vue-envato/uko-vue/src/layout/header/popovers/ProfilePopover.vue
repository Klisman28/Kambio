<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
// SHADCDN COMPONENTS
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
// CUSTOM COMPONENT
import Icon from "@/components/Icon.vue";
// AUTH COMPOSABLE
import { useAuth } from "@/auth/useAuth";

const route = useRoute();
const router = useRouter();
const { state, logout } = useAuth();

const handleLogout = async () => {
  await logout();
  router.replace({
    name: "Login",
    query: { redirect: route.fullPath }
  });
};
</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <div class="flex gap-2 items-center py-2 pr-2 pl-3 rounded-full cursor-pointer bg-hover">
        <p class="text-[13px] font-semibold text-nowrap">
          Hi. {{ state?.user?.displayName || "John Smith" }}
        </p>

        <Avatar size="xs" class="border border-white">
          <AvatarImage v-if="state?.user?.photoURL" :src="state?.user?.photoURL" alt="User" />
          <AvatarFallback>{{ state?.user?.displayName?.charAt(0) }}</AvatarFallback>
        </Avatar>
      </div>
    </PopoverTrigger>

    <PopoverContent class="w-[200px] py-2 px-0 rounded-lg">
      <ul class="text-sm cursor-pointer">
        <li class="flex gap-2 items-center px-5 py-2 transition-all hover:bg-hover">
          <Icon name="User" :size="18" class="text-muted" /> Profile
        </li>

        <li class="flex gap-2 items-center px-5 py-2 transition-all hover:bg-hover">
          <Icon name="Settings" :size="18" class="text-muted" /> Account
        </li>

        <li class="flex gap-2 items-center px-5 py-2 transition-all hover:bg-hover">
          <Icon name="Users" :size="18" class="text-muted" /> Manage Team
        </li>

        <li class="py-1">
          <hr class="border-0 border-b border-b-gray-200 dark:border-b-gray-700" />
        </li>

        <li
          class="flex gap-2 items-center px-5 py-2 transition-all hover:bg-hover"
          @click="handleLogout()">
          <Icon name="LogOut" :size="18" class="text-muted" /> Log Out
        </li>
      </ul>
    </PopoverContent>
  </Popover>
</template>
