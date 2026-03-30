<script setup lang="ts">
import { onMounted, ref } from "vue";
import axios from "axios";
// SHADCN COMPONENTS
import {
  Select,
  SelectItem,
  SelectValue,
  SelectTrigger,
  SelectContent
} from "@/components/ui/select";
// USER STORE
import { useUsers } from "@/stores/users";
// TYPES
import { Status } from "@/types/Status";

const { state } = useUsers();
const statues = ref<Status[]>([]);

const getUserStatues = async () => {
  try {
    const { data } = await axios.get<Status[]>("/api/users/status");
    if (data) statues.value = data;
  } catch (err) {
    console.log(err);
  }
};

onMounted(getUserStatues);
</script>

<template>
  <Select v-model="state.filters.status">
    <SelectTrigger>
      <SelectValue placeholder="Select a Status" />
    </SelectTrigger>

    <SelectContent>
      <SelectItem value="all">All</SelectItem>
      <SelectItem v-for="status in statues" :key="status.id" :value="status.value">
        {{ status.title }}
      </SelectItem>
    </SelectContent>
  </Select>
</template>
