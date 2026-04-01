<script setup lang="ts">
import { toRefs } from "vue";
// SHADCN COMPONENTS
import { Input } from "@/theme/components/ui/input";
import { Button } from "@/theme/components/ui/button";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
// SECTION COMPONENTS
import UserList from "@/theme/sections/users/UserList.vue";
import UserStatusInput from "@/theme/sections/users/UserStatusInput.vue";
// USER STORE
import { useUsers } from "@/theme/stores/users";

const { state } = useUsers();
const { filters } = toRefs(state);
</script>

<template>
  <!-- USER TABLE FILTER ACTIONS -->
  <div class="flex flex-col justify-between gap-4 mt-2 mb-6 md:flex-row md:items-center">
    <div class="flex flex-col items-center gap-3 md:flex-row md:w-3/4 lg:w-2/4">
      <!-- USER SEARCH INPUT -->
      <div class="relative w-full">
        <Input
          v-model="filters.search"
          type="search"
          placeholder="Find User"
          class="rounded-lg ps-9" />

        <Icon
          :size="18"
          name="Search"
          :strokeWidth="2"
          class="absolute inset-y-0 my-auto text-muted start-3" />
      </div>

      <!-- USER STATUS SELECT INPUT -->
      <UserStatusInput />
    </div>

    <Button @click="$router.push('/users/create')">
      <Icon name="Plus" :strokeWidth="2" :size="18" class="me-2" />
      Add User
    </Button>
  </div>

  <!-- USER TABLE SECTION -->
  <UserList />
</template>
